# apps/subscriptions/urls.py
from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('', views.subscription_list, name='subscription_list'),
    path('subscribe/<str:plan_name>/', views.subscribe, name='subscribe'),
    path('current/', views.current_subscription, name='current_subscription'),
]
