from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator

class Cliene(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="nombre")
    apellido = models.CharField(max_length=100, verbose_name="apellido")

    numero_documento = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="nuemro de dni",
        validators= [
            RegexValidator(
                regex='^\d{7,8}$',
                message="El numero de documento solo deben ser numeros"
            )
        ]
    )

    email = models.EmailField(verbose_name= "Correo Electronico", blank=True)

    #telefono y validacion

    telefono = models.CharField(
        max_length=15,
        verbose_name="Telefono",
        validators=[
            RegexValidator(
                regex='^[0-9+()-]+$',
                message="El telefono solo puede contener numeros y los siguientes caracteres: +, -, ( ,"
            )
        ]
    )

    direccion = models.TextField(verbose_name="Direccion", blank=True)
    activo = models.BooleanField(default=True, verbose_name="activo")
    creado = models.DateTimeField(auto_now_add=True, verbose_name="creado")
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["apellido", "nombre"]
        indexes = [
            models.Index(fields=["apellido","nombre"]),
            models.Index(fields=["numero_documento"]),
        ]

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"
    
    def get_absolute_url(self):
        return reverse ("clientes:detalle", kwargs={"pk": self.pk})
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"