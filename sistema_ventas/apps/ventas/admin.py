from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Venta, ItemVenta

class ItemVentaInline(admin.TabularInline):
    model = ItemVenta
    extra = 0
    readonly_fields = ['subtotal']
    fields = ['producto', 'cantidad', 'precio_unitario', 'subtotal']

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['codigo_venta', 'cliente', 'fecha', 'total']
    list_filter = ['fecha', 'cliente']
    search_fields = ['codigo_venta', 'cliente__nombre', 'cliente__apellido']
    readonly_fields = ['fecha', 'total']
    inlines = [ItemVentaInline]
    
    fieldsets = (
        ('Información de la Venta', {
            'fields': ('codigo_venta', 'cliente', 'fecha', 'total')
        }),
    )

@admin.register(ItemVenta)
class ItemVentaAdmin(admin.ModelAdmin):
    list_display = ['venta', 'producto', 'cantidad', 'precio_unitario', 'subtotal']
    list_filter = ['venta__fecha']
    search_fields = ['venta__codigo_venta', 'producto__nombre']