from django.shortcuts import render, redirect
from .models import Subscription, SubscriptionUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import timedelta
from django.utils.timezone import now

@login_required
def subscription_list(request):
    """Muestra los planes de suscripción disponibles y resalta la suscripción activa del usuario."""
    
    # Obtener todos los planes disponibles
    subscriptions = Subscription.objects.all()

    # Obtener la suscripción activa del usuario
    user_subscription = SubscriptionUser.objects.filter(user=request.user).first()

    return render(request, 'subscriptions/subscription_list.html', {
        'subscriptions': subscriptions,
        'user_subscription': user_subscription  # Pasamos la suscripción activa
    })

@login_required
def subscribe(request, plan_name):
    """Permite cambiar entre el plan PREMIUM y GRATUITO para el usuario, actualizando la suscripción existente."""
    
    # Verificar si el plan seleccionado es válido (solo Gratuita o Premium)
    if plan_name not in ['GRATUITA', 'PREMIUM']:
        return redirect('subscriptions:subscription_list')

    # Obtener el plan seleccionado (Gratuita o Premium)
    plan = Subscription.objects.filter(plan_name=plan_name).first()
    if not plan:
        # Si el plan no existe, lo creamos (esto no debería ocurrir con solo 2 planes)
        plan = Subscription.objects.create(plan_name=plan_name, price=0 if plan_name == 'GRATUITA' else 100)

    # Obtener la suscripción actual del usuario (si ya tiene una)
    user_subscription = SubscriptionUser.objects.filter(user=request.user).first()

    if user_subscription:
        # Si el usuario ya tiene una suscripción, la actualizamos
        user_subscription.suscription = plan
        user_subscription.is_free = (plan_name == 'GRATUITA')  # Establecer si es gratuito o premium
        user_subscription.start_date = now()  # Actualizar la fecha de inicio
        user_subscription.save()  # Guardar los cambios
        messages.success(request, f"Suscripción actualizada a {plan_name} correctamente.")
    else:
        # Este caso no debería suceder si todos los usuarios ya tienen suscripción
        messages.error(request, "El usuario no tiene una suscripción activa para actualizar.")
    
    # Redirigir a la página de suscripción actual
    return redirect('subscriptions:current_subscription')


@login_required
def current_subscription(request):
    """Muestra la suscripción actual del usuario."""
    # Obtener la suscripción activa del usuario
    subscription = SubscriptionUser.objects.filter(user=request.user).first()

    if subscription:
        plan = subscription.suscription
        return render(request, 'subscriptions/current_subscription.html', {'subscription': subscription, 'plan': plan})
    else:
        return render(request, 'subscriptions/no_subscription.html')  # Si no tiene suscripción
