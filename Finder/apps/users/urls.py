# apps/users/urls.py
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('client_home/', views.client_home, name='client_home'),
    path('worker_home/', views.worker_home, name='worker_home'),
    path('empresa_home/', views.empresa_home, name='empresa_home'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('list_services/', views.list_services, name='list_services'),
    path('create_service/', views.create_service, name='create_service'),
    path('edit_service/<int:pk>/', views.edit_service, name='edit_service'),
    path('delete_service/<int:pk>/', views.delete_service, name='delete_service'),
    path('search_services/', views.search_services, name='search_services'),
    path('ver_perfil/<int:pk>/', views.ver_perfil, name='ver_perfil'),

]
