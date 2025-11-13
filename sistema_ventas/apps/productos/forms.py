from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields=["nombre", "descripcion", "precio", "stock", "sku", "activo"]
        widgets={
            "descripción":forms.Textarea(attrs={"rows":3}),
            "precio":forms.NumberInput(attrs={"step":"0.01","min":"0"}),
            'stock': forms.NumberInput(attrs={'min': '0'}),
        }
    
    def clean_sku(self):
        sku = self.cleaned_data.get("sku")
        if Producto.objects.filter(sku=sku).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("el Sku ya existe. Por favor ingrese uno unico.")
        return sku