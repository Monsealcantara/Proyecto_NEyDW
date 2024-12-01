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
]
