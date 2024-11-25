# apps/chat/views.py
from django.shortcuts import render
from .models import Message

def chat_view(request):
    messages = Message.objects.filter(receiver=request.user)
    return render(request, 'chat/chat.html', {'messages': messages})
