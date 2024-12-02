# apps/jobs/urls.py
from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('create_quotation/<int:service_id>/', views.create_quotation, name='create_quotation'),  # URL para crear un nuevo trabajo
    path('edit_quotation/<int:pk>/', views.edit_quotation, name='edit_quotation'),
    path('list_quotations/', views.list_quotations, name='list_quotations'),
    path('job_list/', views.job_list, name='job_list'),  # URL para crear un nuevo trabajo
    path('quotation_detail/<int:pk>/', views.quotation_detail, name='quotation_detail'),
    path('quotation_detail_empleado/<int:pk>/', views.quotation_detail_empleado, name='quotation_detail_empleado'),
    path('delete_quotation/<int:pk>/', views.delete_quotation, name='delete_quotation'),
    path('finalize_quotation/<int:pk>/', views.finalize_quotation, name='finalize_quotation'),
    path('contraofertar_quotations/<int:pk>/', views.contraofertar_quotations, name='contraofertar_quotations'),
    path('rechazar_quotations/<int:pk>/', views.rechazar_quotations, name='rechazar_quotations'),
    path('aceptar_quotations/<int:pk>/', views.aceptar_quotations, name='aceptar_quotations'),
    path('rechazar_quotations_cliente/<int:pk>/', views.rechazar_quotations_cliente, name='rechazar_quotations_cliente'),
    path('aceptar_quotations_client/<int:pk>/', views.aceptar_quotations_client, name='aceptar_quotations_client'),
    path('leave_review/<int:pk>/', views.leave_review, name='leave_review'),
]
