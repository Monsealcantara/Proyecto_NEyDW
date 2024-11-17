# materials/models.py
from django.db import models

# Define las empresas que suministran materiales.
class MaterialSupplier(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact_email = models.EmailField()
    logo = models.ImageField(upload_to='supplier_logos/', blank=True, null=True)

# Define los materiales ofrecidos por las empresas.
class Material(models.Model):
    supplier = models.ForeignKey(MaterialSupplier, on_delete=models.CASCADE, related_name='materials')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
