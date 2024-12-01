# materials/models.py
from django.db import models
from apps.users.models import User

# Modelo para los productos
class Material(models.Model):
    empresa = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')  # Relación con el usuario tipo "empresa"
    name = models.CharField(max_length=255)  # Nombre del producto
    description = models.TextField(blank=True, null=True)  # Descripción opcional
    imagen = models.ImageField(upload_to='imagenes_productos/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Precio del producto
    stock = models.PositiveIntegerField()  # Cantidad en inventario

    def __str__(self):
        return self.name