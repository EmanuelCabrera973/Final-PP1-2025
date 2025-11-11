from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "sku", "precio", "stock", "activo", "stock_bajo"]
    list_filter = ["activo", "creado"]
    search_fields = ["nombre", "sku", "descripcion"]
    list_editable = ["precio", "stock", "activo"]
    readonly_fields = ["creado", "actualizado"]

    fieldsets = (
        ("Informacion Basica", {
            "fields": ("nombre", "descripcion", "sku")
        }),
        ("Precio y Stock", {
            "fields": ("precio", "stock")
        }),
        ("Estado", {
            "fields": ("activo",)
        }),
        ("Metadatos", {
            "fields": ("creado", "actualizado"),
            "classes": ("collapse",)
        })
    )


# Register your models here.
