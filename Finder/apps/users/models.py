# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

# Django ya incluye un modelo de usuario en su framework, pero lo extendemos para incluir roles específicos:
class User(AbstractUser):
    ROLE_CHOICES = [
        ('cliente', 'Cliente'),
        ('trabajador', 'Trabajador'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

# Este modelo almacena la información adicional de los trabajadores.
class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='worker_profile')
    profession = models.CharField(max_length=255)  # Plomero, electricista, etc.
    bio = models.TextField(blank=True, null=True)
    gallery = models.ImageField(upload_to='worker_galleries/', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

# Almacena información adicional de los clientes.
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    location = models.CharField(max_length=255)  # Dirección o referencia
