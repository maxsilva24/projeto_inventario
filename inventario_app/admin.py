from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import ItemInventario, Setor, Dependencia
from .resources import ItemInventarioResource

# Register your models here.
@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    class Meta:
        model = Setor
    '''Admin View for '''

    list_display = ('sigla','nome',)
    ordering = ('sigla',)
    search_fields = ('sigla','nome',)
 
@admin.register(Dependencia)
class DependenciaAdmin(admin.ModelAdmin):
    class Meta:
       model = Dependencia

    '''Admin View for '''
    list_display = ('nome_dependencia', 'observacao', )
    list_filter = ('nome_dependencia', )   
    ordering = ('nome_dependencia',)

@admin.register(ItemInventario)
class ItemInventarioAdmin(ImportExportModelAdmin): 
    class Meta:
        model = ItemInventario
        verbose_name = 'Teste'
        verbose_name_plural ='Testes'  

    '''Admin View for '''
    resource_class = ItemInventarioResource 
    '''Admin View for '''
    list_display = ('tombo', 'descricao','item_conferido', 'usuario_nome', 'dependencia_conferencia', 'setor_conferencia',)    
    # fields = ( 'tombo', 'descricao','item_conferido', 'usuario_conferencia', 'dependencia', 'observacao', 'setor', )
    list_filter = ('item_conferido','usuario_conferencia__first_name',)
    search_fields = ('tombo','descricao',)
    readonly_fields = ('tombo', 'descricao', 'usuario_conferencia','valor', 'conta_contabil', 
                       'setor_atual', 'empenho', 'fornecedor', 'numero_documento', 'data_aquisicao',
                        'data_ateste', 'responsavel','dependencia_atual','data_conferencia','data_importacao', )
    fieldsets = (
        ('Item', {
            'fields': (
               'tombo', 'descricao', 
            ),       
        }),
        ('Conferência', {
            'fields': (
               'item_conferido',  
               ('dependencia_conferencia', 'dependencia_atual'),
                'observacao',('setor_conferencia', 'setor_atual'),
               'usuario_conferencia', 'data_conferencia',
                
            ),       
        }),
        ('Detalhes do Item', {
            'classes':('collapse',),
            'fields': (
               'valor', 'conta_contabil', 'empenho', 'fornecedor', 'numero_documento', ('data_aquisicao', 'data_ateste'), 'responsavel', 
               'data_importacao'
            ),       
        }),
    )
    ordering = ('tombo',)

    def save_model(self, request, obj, form, change):
        obj.usuario_conferencia = request.user
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        # return super().has_add_permission(request)
        return False

    def usuario_nome(self, obj):
        return  obj.usuario_conferencia.first_name if obj.usuario_conferencia is not None else ''
    usuario_nome.short_description='Conferido por'