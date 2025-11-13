from django import forms 
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            "nombre",
            "apellido",
            "numero_documento",
            "email",
            "telefono",
            "direccion",
            "activo",
        ]
        widgets = {
            "direccion":forms.Textarea(attrs={"rows":3}),
            "email": forms.EmailInput(attrs={"placeholder":"ejemplo@correo.com"}),
        }
    
    def clean_numero_documento(self):
        numero_documento = self.cleaned_data.get("numero_documento")
        if Cliente.objects.filter(numero_documento=numero_documento).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este DNI ya existe")
        return numero_documento
    
    def clean_email(self):
        email=self.cleaned_data.get("email")
        if email and Cliente.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este correo ya existe")
        return email