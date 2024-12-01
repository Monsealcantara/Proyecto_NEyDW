# apps/materials/urls.py
from django.urls import path
from . import views

app_name = 'venta'

urlpatterns = [
    path('realizar_compra/', views.realizar_compra, name='realizar_compra'),
    path('compra/exitosa/', views.compra_exitosa, name='compra_exitosa'),
    path('compras_lista/', views.compras_lista, name='compras_lista'),
    path('ventas_list/', views.ventas_list, name='ventas_list'),
]
