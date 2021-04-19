from django.contrib import admin, messages
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin  import User

from .models import Dependencia, ItemInventario, Setor
from .resources import ItemInventarioResource
from django.utils.translation import ngettext
from django.utils.datetime_safe import datetime

admin.AdminSite.site_header = 'Administração do Sistema'

# Register your models here.

class ItemInventarioInlineBase(admin.TabularInline):
    '''Tabular Inline View for ItemInventario''' 
           
    model = ItemInventario
    verbose_name_plural = "Itens de Inventário Conferência"
    # search_fields = ('tombo', 'descricao',)
    readonly_fields = ('tombo', 'descricao','item_conferido', 'usuario_nome', 'dependencia_conferencia', 'setor_conferencia', 'dependencia_atual','setor_atual',)
    fieldsets = (
        (None, {
            'fields': (
               'tombo', 'descricao','item_conferido', 'usuario_nome', 'dependencia_conferencia','dependencia_atual', 'setor_conferencia', 'setor_atual',
            ),
        }),
    )
    def has_add_permission(self, request, obj):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    # min_num = 3
    # max_num = 20
    extra = 0
    # raw_id_fields = (,)

class ItemInventarioInlineDependecia(ItemInventarioInlineBase):
    fk_name ='dependencia_conferencia'

class ItemInventarioInlineSetor(ItemInventarioInlineBase):
    fk_name ='setor_conferencia'
@admin.register(Setor)
class SetorAdmin(ImportExportModelAdmin):
    class Meta:
        model = Setor
    '''Admin View for '''
    
    list_display = ('id','sigla','nome', 'contar_itens_inventario_conferidos',
                    'contar_itens_inventario_nao_conferidos','contar_itens_inventario_Total',
                    'contar_itens_inventario_importados', )
    inlines = (ItemInventarioInlineSetor,  )
    ordering = ('sigla',)
    search_fields = ('sigla','nome',)
    readonly_fields = ('contar_itens_inventario_conferidos','contar_itens_inventario_nao_conferidos',
            'contar_itens_inventario_Total','contar_itens_inventario_importados',)
    fieldsets = (
        (None, {
            'fields': (
                'sigla','nome',              
            ),
        }),
        ('Detalhes do Setor', {
            'classes':('collapse',),
            'fields': (
                 'observacao',
            ),
        }),
        ('Relatório da Conferência', {
            'fields': (
                ('contar_itens_inventario_conferidos','contar_itens_inventario_nao_conferidos',
                'contar_itens_inventario_Total'),'contar_itens_inventario_importados',
            ),
        }),
    )
    def has_import_permission(self, request):
        return False

@admin.register(Dependencia)
class DependenciaAdmin(ImportExportModelAdmin):
    class Meta:
       model = Dependencia    
    '''Admin View for '''
    list_display = ('id','nome_dependencia', 'contar_itens_inventario_conferidos',
                    'contar_itens_inventario_nao_conferidos','contar_itens_inventario_Total',
                    'contar_itens_inventario_importados', )
    # list_filter = ('nome_dependencia', )  
    list_display_links =('id','nome_dependencia',)     
    search_fields = ('id','nome_dependencia',)
    ordering = ('nome_dependencia',)
    inlines = (ItemInventarioInlineDependecia,  )
    readonly_fields = ('contar_itens_inventario_conferidos','contar_itens_inventario_nao_conferidos',
            'contar_itens_inventario_Total','contar_itens_inventario_importados',)
    fieldsets = (
        (None, {
            'fields': (
                'nome_dependencia',                
            ),
        }),
        ('Detalhes da Dependência', {
            'classes':('collapse',),
            'fields': (
                 'descricao_local', 'observacao', 
            ),
        }),
        ('Relatório da Conferência', {
            'fields': (
                ('contar_itens_inventario_conferidos','contar_itens_inventario_nao_conferidos',
                'contar_itens_inventario_Total'),'contar_itens_inventario_importados',
            ),
        }),
    )
    def has_import_permission(self, request):
        return False


@admin.register(ItemInventario)
class ItemInventarioAdmin(ImportExportModelAdmin): 
    class Meta:
        model = ItemInventario

    '''Admin View for '''
    resource_class = ItemInventarioResource 
    '''Admin View for '''
    list_display = ('tombo', 'descricao','item_conferido', 'usuario_nome', 'data_conferencia','dependencia_conferencia', 'setor_conferencia',)    
    list_display_links =('tombo','descricao','dependencia_conferencia', 'setor_conferencia',)
    # list_select_related =('setor_conferencia','dependencia_conferencia', )
    list_filter = ('item_conferido','usuario_conferencia__first_name', 'dependencia_conferencia', 'setor_conferencia',)
    search_fields = ('tombo','descricao',)
    # raw_id_fields =('dependencia_conferencia',)
    # autocomplete_fields =('dependencia_conferencia',)
    actions = ['conferir_varios_itens']
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
        return False

    def conferir_varios_itens(self, request, queryset):        
        updated = queryset.update(item_conferido=True, usuario_conferencia =request.user, data_conferencia= datetime.now() )
        self.message_user(request, ngettext(
            '%d Item de Inventário foi conferido com sucesso.',
            '%d Itens de Inventário foi conferido com sucesso',
            updated,
        ) % updated, messages.SUCCESS) 
    conferir_varios_itens.short_description = 'Conferir itens selecionados'


