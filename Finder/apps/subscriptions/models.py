# subscriptions/models.py
from django.db import models
from apps.users.models import User

# Manejo de planes de suscripción.
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan_name = models.CharField(max_length=50)  # Gratuita o Premium
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
 