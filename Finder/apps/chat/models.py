# chat/models.py
from django.db import models
from apps.users.models import User, Service
from apps.jobs.models import  Quotation

class Chat(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, null=True)
    participants = models.ManyToManyField(User)  # Los dos participantes del chat
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación del chat
    is_activate = models.BooleanField(default=True)
    def __str__(self):
        return f"Chat entre {', '.join([user.username for user in self.participants.all()])}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Mensaje de {self.sender.username} a {self.receiver.username} ({self.timestamp})"
