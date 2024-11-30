# apps/jobs/urls.py
from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='job_list'),  #mostrar trabajos
    path('create/', views.create_job, name='create_job'),  # URL para crear un nuevo trabajo
    path('<int:job_id>/', views.job_detail, name='job_detail'), #detalles del trabajo
]
