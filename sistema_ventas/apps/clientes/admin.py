from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ["nombre_comleto", "numero_documento","email", "telefono", "activo"]
    list_filter = ["activo","creado"]
    search_fields = ["nombre","apellido", "numero_documento","email"]
    list_editable = ["activo"]
    readonly_fields = ["creado", "actualizado"]

    fieldsets = (
        ("Datos Personales",{
            "fields":("nombre","apellido","numero_documento")
        }),
        ("contacto",{
            "fields":("email","telefono","direccion")
        }),
        ("Estado",{
            "fields": ("activo",)
        })
        ("Metadatos",{
            "fields":("creado","actualizado"),
            "classes":("collapse",)
        })

    )

# Register your models here.
