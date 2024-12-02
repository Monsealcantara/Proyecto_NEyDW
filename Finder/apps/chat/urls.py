# apps/chat/urls.py
from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('chat_list/', views.chat_list, name='chat_list'),
    path('chat_detail/<int:id>/', views.chat_detail, name='chat_detail'),
]
