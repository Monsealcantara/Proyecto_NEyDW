# apps/chat/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from django.utils import timezone

def chat_list(request):
    """Vista para listar todos los chats del usuario"""
    # Filtrar chats en los que el usuario es participante
    chats = Chat.objects.filter(participants=request.user)
    
    return render(request, 'chat/chat_list.html', {'chats': chats})


@login_required
def chat_detail(request, id):
    """Vista para ver un chat específico y enviar nuevos mensajes"""
    # Obtener el chat por ID
    chat = get_object_or_404(Chat, id=id)

    # Verificar que el usuario sea un participante del chat
    if request.user not in chat.participants.all():
        return redirect('chat:chat_list')  # Si el usuario no es parte del chat, redirige a la lista
    
    # Obtener todos los mensajes del chat, ordenados por fecha de creación
    messages = chat.messages.all().order_by('timestamp')

    # Obtener el otro participante (que no es el usuario actual)
    other_participant = chat.participants.exclude(id=request.user.id).first()

    # Procesar el formulario de envío de un nuevo mensaje
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            # Crear un nuevo mensaje
            Message.objects.create(
                chat=chat,
                sender=request.user,
                receiver=other_participant,  # El receptor es el otro participante
                content=content
            )
            return redirect('chat:chat_detail', id=chat.id)  # Redirigir para mostrar el nuevo mensaje
    
    # Renderizar la página con los mensajes y el otro participante
    return render(request, 'chat/chat_detail.html', {'chat': chat, 'messages': messages, 'other_participant': other_participant})