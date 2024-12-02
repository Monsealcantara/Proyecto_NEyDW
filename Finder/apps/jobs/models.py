# jobs/models.py
from django.db import models
from apps.users.models import Client, Worker, Service

class Quotation(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='quotations')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='quotations')
    description = models.TextField()  # Descripción original del trabajo
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Presupuesto inicial
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Precio de la cotización actual
    time_estimate = models.CharField(max_length=255)  # Tiempo estimado para realizar el trabajo
    accepted = models.BooleanField(default=False)   # Si el cliente acepta la cotización
    location = models.CharField(max_length=255)  # Ubicación del trabajo
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # Latitud
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # Longitud
    is_active = models.BooleanField(default=True)  # Indica si la cotización está activa o no
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha en que se crea la cotización
    counter_offer = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)  # Contraoferta del trabajador
    counter_offer_accepted = models.BooleanField(default=False)  # Si el cliente acepta la contraoferta

    def __str__(self):
        return f"Cotización de {self.client.user.username} para {self.service.name}"

# Guarda las reseñas de los trabajos realizados.
class Review(models.Model):
    quotation = models.OneToOneField(Quotation, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='reviews')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(blank=True, null=True)  # Rango: 1-5
    status = models.TextField(default=True)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)    
    
    def __str__(self):
        return f"Calificacion de {self.client.user.username} para {self.service.name}"
