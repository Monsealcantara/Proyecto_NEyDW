from django.db import models
from django.contrib.auth.models import User
from apps.materials.models import *

# Modelo para el ítem del Carrito
class ItemCarrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items_carrito')
    producto = models.ForeignKey(Material, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.producto.nombre} x{self.cantidad}"

# Modelo para el Carrito
class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carritos')
    items = models.ManyToManyField(ItemCarrito)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"
