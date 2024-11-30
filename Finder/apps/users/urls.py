# apps/users/urls.py
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('client_home/', views.client_home, name='client_home'),
    path('worker_home/', views.worker_home, name='worker_home'),
]
