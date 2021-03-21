from .models import ItemInventario,Dependencia, Setor 
from django.contrib.auth.admin import User
from django.conf import settings
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget, FloatWidget, IntegerWidget, DateWidget, BooleanWidget, DateTimeWidget
from django.contrib.auth.models import UserManager
from django.utils import timezone

class ItemInventarioResource(resources.ModelResource):
    valorTZ = settings.USE_TZ
    tombo           = fields.Field(attribute='tombo',column_name='Tombo')
    descricao       = fields.Field(attribute='descricao',column_name='Descrição')
    # 
    item_conferido     = fields.Field(attribute='item_conferido',column_name='Item Conferido?', widget=BooleanWidget())
    usuario_conferencia  = fields.Field(attribute='usuario_conferencia',column_name='Conferido Por:', widget=ForeignKeyWidget(User, field= 'first_name'))
    data_conferencia= fields.Field(attribute='data_conferencia',column_name='Data conferência', widget=DateTimeWidget())
    observacao       = fields.Field(attribute='observacao',column_name='Observação')
    # 
    valor           = fields.Field(attribute='valor',column_name='Valor (R$)', widget=FloatWidget())
    conta_contabil  = fields.Field(attribute='conta_contabil',column_name='Conta Contábil', widget=IntegerWidget())
    setor_atual     = fields.Field(attribute='setor_atual',column_name='Setor',  widget=ForeignKeyWidget(Setor, field='sigla'))
    empenho         = fields.Field(attribute='empenho',column_name='Empenho')
    fornecedor      = fields.Field(attribute='fornecedor',column_name='Fornecedor')
    numero_documento= fields.Field(attribute='numero_documento',column_name='Número Documento' )
    data_aquisicao  = fields.Field(attribute='data_aquisicao',column_name='Data Aquisição', widget=DateWidget())
    data_ateste     = fields.Field(attribute='data_ateste',column_name='Data Ateste', widget=DateWidget())
    dependencia_atual     = fields.Field(attribute='dependencia_atual',column_name='Dependência', widget=ForeignKeyWidget(Dependencia, field= 'nome_dependencia'))
    responsavel     = fields.Field(attribute='responsavel',column_name='Responsável')   

    class Meta:
        model = ItemInventario
        # documentação do meta dados
        #    https://django-import-export.readthedocs.io/en/latest/api_resources.html     
        # batch_size = 100 #lotes de 100 dados
        # use_bulk = True
        import_id_fields  = ('tombo',)
        #if you want to exclude any field from exporting
        exclude = ('id','usuario_conferencia', 'setor_conferencia', 'observacao','data_importacao', )    
        fields = ( 'tombo','descricao',
                   'item_conferido','usuario_conferencia','data_conferencia','observacao',
                   'valor', 'conta_contabil','setor_atual',  'empenho', 
                   'fornecedor', 'numero_documento', 'data_aquisicao', 
                   'data_ateste', 'dependencia_atual','responsavel',  )
        # fields = ( 'tombo','descricao','valor', 'setor_atual')
        #Order of the export fields
        export_order = fields

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        return super().before_import(dataset, using_transactions, dry_run, **kwargs)
        
    def before_import_row(self, row, **kwargs):
        settings.USE_TZ = False
        item_conferido = row.get('Item Conferido?') 
        if item_conferido is not None:       
            if item_conferido.upper() in ["NÃO", "N", "NAO"]:
                row['Item Conferido?'] = False
            elif item_conferido.upper() in ["SIM", "S", "Sim"]:
                row['Item Conferido?'] = True
        #
        setor = row.get('Setor')
        if setor is not None:
            (setor, _created) = Setor.objects.get_or_create(sigla=setor)
            row['Setor'] = setor.sigla
        # 
        dependencia = row.get('Dependência')
        if dependencia is not None:
            (dependencia, _created) = Dependencia.objects.get_or_create(nome_dependencia=dependencia)
            row['Dependência'] = dependencia.nome_dependencia  
        
        nome_usuario = row.get('Conferido Por:')
        if nome_usuario is not None and nome_usuario !='' :
            (usuario, _created) = User.objects.get_or_create(first_name=nome_usuario)
            if _created == True or usuario.username =='':
                usuario.username = nome_usuario.replace(' ', '_')
                usuario.set_password('sigo1234')  
                usuario.save()          
            row['Conferido Por:'] = usuario.first_name  
        
        return super().before_import_row(row, **kwargs)    
    
    def before_save_instance(self, instance, using_transactions, dry_run):
        if  instance.setor_conferencia == None  and instance.setor_atual !=None:
            instance.setor_conferencia = instance.setor_atual

        if  instance.dependencia_conferencia == None  and instance.dependencia_atual !=None:
            instance.dependencia_conferencia = instance.dependencia_atual

        return super().before_save_instance(instance, using_transactions, dry_run)
    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        settings.USE_TZ = self.valorTZ
        return super().after_import(dataset, result, using_transactions, dry_run, **kwargs)

    def import_data_only_XLSX(self):
        import tablib
        import os
        from max_sis_if.resources import ItemInventarioResource
        from max_sis_if.models import ItemInventario
        from io import BytesIO
        import openpyxl
        # from tqdm import tqdm
        end_arquivo = os.path.join(os.getcwd(),'arquivos_tmp','2021_planilha_inventario_final_Macro2.xlsm')    
        arq = open(end_arquivo, 'rb').read()
        xlsx_book = openpyxl.load_workbook(BytesIO(arq), read_only=True, data_only=True)
        dataset_tab = tablib.Dataset()
        sheet = xlsx_book.active
        # obtain generator
        rows = sheet.rows
        dataset_tab.headers = [cell.value for cell in next(rows)]
        for row in rows:
            row_values = [cell.value for cell in row]
            dataset_tab.append(row_values)            
        # print(dataset_tab)
        # print(dataset_tab.headers)
        result = ItemInventarioResource().import_data(dataset_tab, dry_run=False, raise_errors=True )
        print(result.has_errors())



