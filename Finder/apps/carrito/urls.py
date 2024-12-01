# apps/materials/urls.py
from django.urls import path
from . import views

app_name = 'carrito'

urlpatterns = [
    path('ver_carrito', views.ver_carrito, name='ver_carrito'),
    path('agregar_carrito/<int:id>/', views.agregar_carrito, name='agregar_carrito'),
    path('incrementar_cantidad_producto_carrito/<int:id>/', views.incrementar_cantidad_producto_carrito, name='incrementar_cantidad_producto_carrito'),
    path('decrementar_cantidad_producto_carrito/<int:id>/', views.decrementar_cantidad_producto_carrito, name='decrementar_cantidad_producto_carrito'),
    path('eliminar_producto_carrito/<int:id>/', views.eliminar_producto_carrito, name='eliminar_producto_carrito'),
]
