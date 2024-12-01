# apps/materials/urls.py
from django.urls import path
from . import views

app_name = 'materials'

urlpatterns = [
    path('agregar_material/', views.agregar_material, name='agregar_material'),
    path('editar_material/<int:id>/', views.editar_material, name='editar_material'),
    path('eliminar_material/<int:id>/', views.eliminar_material, name='eliminar_material'),

]
