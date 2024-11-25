# apps/materials/urls.py
from django.urls import path
from . import views

app_name = 'materials'

urlpatterns = [
    path('', views.material_list, name='material_list'),
]
