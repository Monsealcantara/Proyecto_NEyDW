from django.contrib.auth.models import AbstractUser
from django.db import models

# Extensión del modelo User para incluir roles específicos
class User(AbstractUser):
    ROLE_CHOICES = [
        ('cliente', 'Cliente'),
        ('trabajador', 'Trabajador'),
        ('empresa', 'Empresa'), 
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username


# Modelo para almacenar los servicios que los trabajadores ofrecen
class Service(models.Model):
    worker = models.ForeignKey('Worker', on_delete=models.CASCADE, related_name='services')  # Un trabajador puede tener muchos servicios
    name = models.CharField(max_length=255)  # Nombre del servicio (Ej. Electricista, Plomero, etc.)
    description = models.TextField(blank=True, null=True)  # Descripción opcional del servicio
    keywords = models.ManyToManyField('Keyword', related_name='services', blank=True)  # Palabras clave asociadas con el servicio

    def __str__(self):
        return self.name


# Modelo para representar las palabras clave que pueden asociarse con los servicios
class Keyword(models.Model):
    word = models.CharField(max_length=100, unique=True)  # Palabra clave (ej. "urgente", "económico", etc.)

    def __str__(self):
        return self.word


# Relación entre Worker y Service, ya que un trabajador puede ofrecer varios servicios
class WorkerService(models.Model):
    worker = models.ForeignKey('Worker', on_delete=models.CASCADE, related_name='worker_services')
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='worker_services')

    def __str__(self):
        return f"{self.worker.user.username} ofrece {self.service.name}"


# Información adicional sobre el trabajador
class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='worker_profile')  # Relación uno a uno con User
    profession = models.CharField(max_length=255)  # Ejemplo: Electricista, Plomero, etc.
    bio = models.TextField(blank=True, null=True)
    gallery = models.ImageField(upload_to='worker_galleries/', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)  # Calificación del trabajador

    def __str__(self):
        return self.user.username
        
# Almacena información adicional sobre los clientes
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    location = models.CharField(max_length=255)  # Dirección o ubicación del cliente

    def __str__(self):
        return self.user.username
