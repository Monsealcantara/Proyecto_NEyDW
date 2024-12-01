from django.db import models
from apps.venta.models import *
from django.contrib.auth.models import User
from apps.materials.models import *

# Modelo para el ítem de Venta
class ItemVenta(models.Model):
    producto = models.ForeignKey(Material, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=6, decimal_places=2)  # Precio al momento de la venta

    def __str__(self):
        return f"{self.producto.nombre} x{self.cantidad}"
    
    class Meta:
        verbose_name = "item_venta"
        verbose_name_plural = "items_ventas"
        ordering=['cantidad']
        unique_together=('producto','precio')

# Modelo para Venta
class Venta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ventas')
    items = models.ManyToManyField(ItemVenta)
    fecha_venta = models.DateTimeField(auto_now_add=True)

    def total_venta(self):
        return sum(item.cantidad * item.precio for item in self.items.all())

    def __str__(self):
        return f"Venta {self.id} a {self.usuario.username}"
