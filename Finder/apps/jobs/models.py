# jobs/models.py
from django.db import models
from apps.users.models import Client, Worker

# Define las solicitudes de trabajos creadas por los clientes.
class Job(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    keywords = models.CharField(max_length=255)  # Para filtros

# Define las propuestas de los trabajadores para un trabajo.
class Quotation(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='quotations')
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='quotations')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    time_estimate = models.CharField(max_length=255)  # Tiempo estimado para realizar el trabajo
    accepted = models.BooleanField(default=False)

# Guarda las reseñas de los trabajos realizados.
class Review(models.Model):
    job = models.OneToOneField(Job, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='reviews')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()  # Rango: 1-5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
