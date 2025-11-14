from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.db.models import Sum, F
from apps.clientes.models import Cliente
from apps.productos.models import Producto

class Venta(models.Model):
    codigo_venta = models.CharField(
        max_length=20,
        unique= True,
        verbose_name="Codigo de venta"
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        verbose_name="Cliente"
    )
    fecha = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de venta"
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places = 2,
        default = 0,
        validators=[MinValueValidator(0)],
        verbose_name="Total de la venta"
    )
    class Meta:
        verbose_name ="Venta"
        verbose_name_plural = "Ventas"
        ordering = ["-fecha"]

    def __str__(self):
        return f"Venta {self.codigo_venta} - Cliente: {self.cliente.nombre}"
    
    def get_absolute_url(self):
        return reverse("ventas:detalle", kwargs={"pk": self.pk})
    
    def calcular_total(self):
        """Calcula el total de la venta sumando los totales de los detalles de venta."""
        total = self.items.aggregate(
            total=Sum(F("cantidad") * F("precio_unitario"))
        )["total"] or 0
        self.total = total
        self.save()
        return total
    
class ItemVenta(models.Model):
    venta = models.ForeignKey(
        Venta, 
        on_delete=models.CASCADE,
        related_name='items'
    )
    producto = models.ForeignKey(
        Producto, 
        on_delete=models.PROTECT,
        verbose_name="Producto"
    )
    cantidad = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Cantidad"
    )
    precio_unitario = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Precio Unitario",
        null=True,  # ← Permitir null temporalmente
        blank=True
    )
    subtotal = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Subtotal"
    )
    
    class Meta:
        verbose_name = "Item de Venta"
        verbose_name_plural = "Items de Venta"
    
    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"
    
    def save(self, *args, **kwargs):
        # Si no tiene precio_unitario, usar el precio actual del producto
        if not self.precio_unitario and self.producto_id:
            self.precio_unitario = self.producto.precio
        
        # Calcular subtotal automáticamente (solo si tenemos ambos valores)
        if self.cantidad and self.precio_unitario:
            self.subtotal = self.cantidad * self.precio_unitario
        else:
            self.subtotal = 0
        
        super().save(*args, **kwargs)
        
        # Recalcular el total de la venta
        if self.venta_id:
            self.venta.calcular_total()
    
    def delete(self, *args, **kwargs):
        venta = self.venta
        super().delete(*args, **kwargs)
        # Recalcular el total después de eliminar
        venta.calcular_total()