# apps/notifications/views.py
from django.shortcuts import render
from .models import Notification

def notification_list(request):
    """Muestra las notificaciones del usuario actual."""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})

def mark_as_read(request, notification_id):
    """Marca una notificación como leída."""
    notification = Notification.objects.get(id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications:notification_list')
