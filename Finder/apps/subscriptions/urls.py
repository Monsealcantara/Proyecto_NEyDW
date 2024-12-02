from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('list/', views.subscription_list, name='subscription_list'),  # Listar los planes disponibles
    path('subscribe/<str:plan_name>/', views.subscribe, name='subscribe'),  # Cambiar plan
    path('current/', views.current_subscription, name='current_subscription'),  # Ver suscripción actual
]
