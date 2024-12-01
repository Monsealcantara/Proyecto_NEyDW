# subscriptions/models.py
from django.db import models
from apps.users.models import User

# Manejo de planes de suscripción.
class Subscription(models.Model):
    plan_name = models.CharField(max_length=50) 
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.plan_name} - ${self.price}"

    class Meta:
        verbose_name = "Plan de Suscripción"
        verbose_name_plural = "Planes de Suscripción"

# Suscripcion de usuario.
class SubscriptionUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    suscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='subscriptions')
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    is_free = models.BooleanField(default=False)  # Determina si es un plan gratuito
    
    def __str__(self):
        return f"Suscripción de {self.user.username} - {self.suscription.plan_name}"

    class Meta:
        verbose_name = "Suscripción de Usuario"
        verbose_name_plural = "Suscripciones de Usuarios"