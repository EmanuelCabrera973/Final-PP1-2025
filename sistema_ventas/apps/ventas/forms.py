from django import forms
from django.forms import inlineformset_factory
from .models import Venta, ItemVenta
from apps.productos.models import Producto

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
        }

class ItemVentaForm(forms.ModelForm):
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.filter(activo=True, stock__gt=0),
        widget=forms.Select(attrs={'class': 'form-control producto-select'}),
        empty_label="Seleccione un producto"
    )
    
    class Meta:
        model = ItemVenta
        fields = ['producto', 'cantidad']
        widgets = {
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control cantidad-input',
                'min': '1',
                'value': '1'  # ← Valor por defecto
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')
        cantidad = cleaned_data.get('cantidad')
        
        # Si no hay producto, no validar (form vacío)
        if not producto:
            return cleaned_data
            
        if cantidad and cantidad > producto.stock:
            raise forms.ValidationError(
                f"Stock insuficiente para {producto.nombre}. Solo hay {producto.stock} unidades disponibles."
            )
        
        return cleaned_data

# Formset para los items de venta
ItemVentaFormSet = inlineformset_factory(
    Venta,
    ItemVenta,
    form=ItemVentaForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True
)