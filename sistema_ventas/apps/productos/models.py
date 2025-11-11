from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator

class Producto(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Producto")
    descripcion = models.TextField(blank= True, verbose_name="Descripción del Producto")
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Precio"
    )
    stock = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="Cantidad en Stock",
        default = 0
    )
    sku = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="SKU"
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")
    creado = models.DateTimeField(auto_now_add = True)
    actualizado= models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']
    def __str__(self):
        return f"{self.nombre} (SKU: {self.sku})"
    def get_absolute_url(self):
        return reverse("preoductos:detalle", kwargs={"pk":self.pk})
    
    @property
    def stock_bajo(self):
        """si el stock es menor a 10 unidades"""
        return self.stock < 10
# Create your models here.
