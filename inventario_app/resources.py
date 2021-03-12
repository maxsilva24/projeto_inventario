from .models import ItemInventario,Dependencia, Setor 
from django.contrib.auth.admin import User
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget, FloatWidget, IntegerWidget, DateWidget, BooleanWidget, DateTimeWidget
from django.contrib.auth.models import UserManager

class ItemInventarioResource(resources.ModelResource):

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
    empenho         = fields.Field(attribute='empenho',column_name='Empenho',widget=IntegerWidget() )
    fornecedor      = fields.Field(attribute='fornecedor',column_name='Fornecedor')
    numero_documento= fields.Field(attribute='numero_documento',column_name='Número Documento',widget=IntegerWidget() )
    data_aquisicao  = fields.Field(attribute='data_aquisicao',column_name='Data Aquisição', widget=DateWidget())
    data_ateste     = fields.Field(attribute='data_ateste',column_name='Data Ateste', widget=DateWidget())
    dependencia_atual     = fields.Field(attribute='dependencia_atual',column_name='Dependência', widget=ForeignKeyWidget(Dependencia, field= 'nome_dependencia'))
    responsavel     = fields.Field(attribute='responsavel',column_name='Responsável')   

    class Meta:
        model = ItemInventario
        # exclude = ('imported', )
        #skip_unchanged = True
        #report_skipped = True
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

    def before_import_row(self, row, **kwargs):
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
        if nome_usuario is not None:
            (usuario, _created) = User.objects.get_or_create(first_name=nome_usuario)
            usuario.username = nome_usuario.replace(' ', '_')
            usuario.set_password('sigo1234')            
            row['Conferido Por:'] = usuario.first_name  

        return super().before_import_row(row, **kwargs)    
    
    def before_save_instance(self, instance, using_transactions, dry_run):
        if  instance.setor_conferencia == None  and instance.setor_atual !=None:
            instance.setor_conferencia = instance.setor_atual

        if  instance.dependencia_conferencia == None  and instance.dependencia_atual !=None:
            instance.dependencia_conferencia = instance.dependencia_atual

        return super().before_save_instance(instance, using_transactions, dry_run)
    
