# apps/subscriptions/views.py
from django.shortcuts import render, redirect
from .models import Subscription
from django.utils.timezone import now

def subscription_list(request):
    """Muestra los planes de suscripción disponibles."""
    subscriptions = [
        {'name': 'Gratuita', 'price': 0, 'benefits': ['Acceso limitado a funciones']},
        {'name': 'Premium', 'price': 100, 'benefits': ['Acceso completo a funciones', 'Descuento en comisiones']},
    ]
    return render(request, 'subscriptions/subscription_list.html', {'subscriptions': subscriptions})

def subscribe(request, plan_name):
    """Suscribe al usuario al plan seleccionado."""
    if plan_name not in ['Gratuita', 'Premium']:
        return redirect('subscriptions:subscription_list')
    
    price = 0 if plan_name == 'Gratuita' else 100
    Subscription.objects.create(user=request.user, plan_name=plan_name, start_date=now(), end_date=now().replace(month=now().month + 1), price=price)
    return redirect('subscriptions:current_subscription')

def current_subscription(request):
    """Muestra la suscripción actual del usuario."""
    subscription = Subscription.objects.filter(user=request.user).last()
    return render(request, 'subscriptions/current_subscription.html', {'subscription': subscription})
