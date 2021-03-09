from django.contrib import admin
from .models import ItemInventario

# Register your models here.
@admin.register(ItemInventario)
class ItemInventarioAdmin(admin.ModelAdmin):
    pass
    '''Admin View for '''
    # list_display = ('',)
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)