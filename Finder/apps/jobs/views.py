# apps/jobs/views.py
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import QuotationForm, CounterOfferForm, EditQuotationForm
from .models import  Quotation
from apps.users.models import Service, User, Client
from apps.chat.models import Message, Chat
from apps.notifications.models import Notification

@login_required
def create_quotation(request, service_id):
    service = Service.objects.get(id=service_id)

    if request.method == 'POST':
        form = QuotationForm(request.POST)
        if form.is_valid():
            quotation = form.save(commit=False)
            quotation.client = Client.objects.get(user=request.user)
            quotation.service = service
            # Asignar latitud y longitud si se pasan desde el formulario
            quotation.latitude = request.POST.get('latitude')
            quotation.longitude = request.POST.get('longitude')
            quotation.save()

            # Crear una notificación para el cliente
            notification_message = f"El cliente {request.user} ha creado una oferta de trabajo'."
            Notification.objects.create(
                user=quotation.service.worker.user,  # Enviamos la notificación al cliente que publicó el trabajo
                message=notification_message,
                is_read=False
            ) 

            return redirect('jobs:list_quotations')
    else:
        form = QuotationForm()

    return render(request, 'jobs/create_quotation.html', {'form': form, 'service': service})

@login_required
def edit_quotation(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    if request.user != quotation.client.user:
        return redirect('jobs:list_quotations')

    if request.method == 'POST':
        form = QuotationForm(request.POST, instance=quotation)
        if form.is_valid():
            quotation = form.save(commit=False)
            # Actualizar latitud y longitud si se envían en el formulario
            quotation.latitude = request.POST.get('latitude')
            quotation.longitude = request.POST.get('longitude')
            quotation.save()
            return redirect('jobs:quotation_detail', pk=quotation.pk)
    else:
        form = QuotationForm(instance=quotation)

    return render(request, 'jobs/edit_quotation.html', {'form': form, 'quotation': quotation})

@login_required
def job_list(request):
    quotations = Quotation.objects.filter(service__worker__user=request.user)
    return render(request, 'jobs/job_list.html', {'quotations': quotations})

@login_required
def list_quotations(request):
    client = Client.objects.get(user=request.user)
    quotations = Quotation.objects.filter(client=client)
    return render(request, 'jobs/list_quotations.html', {'quotations': quotations})

@login_required
def quotation_detail(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    return render(request, 'jobs/quotation_detail.html', {'quotation': quotation})


@login_required
def quotation_detail_empleado(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    return render(request, 'jobs/quotation_detail_empleado.html', {'quotation': quotation})

@login_required
def delete_quotation(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)

    # Asegúrate de que el cliente o el trabajador puedan eliminar la cotización
    if request.user != quotation.client.user and request.user != quotation.worker.user:
        messages.error(request, "No tienes permisos para eliminar esta cotización.")
        return redirect('jobs:list_quotations')

    # Elimina la cotización
    quotation.delete()
    messages.success(request, "Cotización eliminada correctamente.")
    return redirect('jobs:list_quotations')

@login_required
def contraofertar_quotations(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    
    # Verificamos que el trabajador que hace la contraoferta sea el trabajador de la cotización
    if request.user != quotation.service.worker.user:
        return redirect('jobs:job_list')

    if request.method == 'POST':
        form = CounterOfferForm(request.POST, instance=quotation)
        if form.is_valid():
            quotation = form.save(commit=False)
            # Actualizar latitud y longitud si se envían en el formulario
            quotation.latitude = request.POST.get('latitude')
            quotation.longitude = request.POST.get('longitude')
            quotation.save()
            
            # Crear una notificación para el cliente
            notification_message = f"El trabajador {quotation.service.worker.user.username} ha contraofertado su propuesta para el trabajo '{quotation.service.name}'."
            Notification.objects.create(
                user=quotation.client.user,  # Enviamos la notificación al cliente que publicó el trabajo
                message=notification_message,
                is_read=False
            )
            
            # Redirigimos al detalle de la cotización después de guardar
            return redirect('jobs:quotation_detail_empleado', pk=quotation.pk)
    else:
        form = CounterOfferForm(instance=quotation)

    return render(request, 'jobs/contraofertar_quotations.html', {'form': form, 'quotation': quotation})

@login_required
def rechazar_quotations(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)

    # Asegúrate de que solo el cliente pueda finalizar una cotización
    if request.user != quotation.service.worker.user:
        messages.error(request, "No tienes permisos para finalizar esta cotización.")
        return redirect('jobs:job_list')

    # Cambiar el estado de is_active a False
    quotation.is_active = False
    quotation.save()

    # Crear una notificación para el cliente
    notification_message = f"El trabajador {quotation.service.worker.user.username} rechazo la propuesta para el trabajo '{quotation.service.name}'."
    Notification.objects.create(
        user=quotation.client.user,  # Enviamos la notificación al cliente que publicó el trabajo
        message=notification_message,
        is_read=False
    )
            
    messages.success(request, "Oferta rechazada correctamente.")
    return redirect('jobs:job_list')

@login_required
def aceptar_quotations(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)

    # Asegúrate de que solo el cliente pueda finalizar una cotización
    if request.user != quotation.service.worker.user:
        messages.error(request, "No tienes permisos para finalizar esta cotización.")
        return redirect('jobs:job_list')

    # Cambiar el estado de is_active a False
    quotation.accepted = True
    quotation.save()

    # Crear un nuevo chat entre el cliente y el trabajador
    chat = Chat.objects.create()
    chat.participants.add(quotation.client.user, quotation.service.worker.user)

    # Enviar un mensaje inicial en el chat
    Message.objects.create(
        chat=chat,
        sender=quotation.service.worker.user,
        receiver=quotation.client.user,
        content="Hola, tu oferta ha sido aceptada. ¿Cómo podemos continuar?",
        is_read=False
    )
    
    # Crear una notificación para el cliente
    notification_message = f"El trabajador {quotation.service.worker.user.username} acepto la propuesta para el trabajo '{quotation.service.name}'."
    Notification.objects.create(
        user=quotation.client.user,  # Enviamos la notificación al cliente que publicó el trabajo
        message=notification_message,
        is_read=False
    )

     # Crear una notificación para el cliente
    notification_message = f"El trabajador {quotation.service.worker.user.username} ha iniciado un chat contigo."
    Notification.objects.create(
        user=quotation.client.user,  # Enviamos la notificación al cliente que publicó el trabajo
        message=notification_message,
        is_read=False
    )

    messages.success(request, "Oferta aceptada correctamente.")
    return redirect('jobs:job_list')

@login_required
def rechazar_quotations_cliente(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)

    # Asegúrate de que solo el cliente pueda finalizar una cotización
    if request.user != quotation.client.user:
        messages.error(request, "No tienes permisos para finalizar esta cotización.")
        return redirect('jobs:job_list')

    # Cambiar el estado de is_active a False
    quotation.is_active = False
    quotation.save()

    # Crear una notificación para el cliente
    notification_message = f"El cliente {quotation.client.user.username} rechazo la contraoferta para el trabajo '{quotation.service.name}'."
    Notification.objects.create(
        user=quotation.service.worker.user,  # Enviamos la notificación al cliente que publicó el trabajo
        message=notification_message,
        is_read=False
    )

    messages.success(request, "Cotización rechazada correctamente.")
    return redirect('jobs:list_quotations')

@login_required
def aceptar_quotations_client(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)

    # Asegúrate de que solo el cliente pueda finalizar una cotización
    if request.user != quotation.client.user:
        messages.error(request, "No tienes permisos para finalizar esta cotización.")
        return redirect('jobs:job_list')

    # Cambiar el estado de is_active a False
    quotation.counter_offer_accepted = True
    quotation.save()

    # Crear un nuevo chat entre el cliente y el trabajador
    chat = Chat.objects.create()
    chat.participants.add(quotation.client.user, quotation.service.worker.user)

    # Enviar un mensaje inicial en el chat
    Message.objects.create(
        chat=chat,
        sender=quotation.client.user,
        receiver=quotation.service.worker.user,
        content="Hola, tu contraoferta ha sido aceptada. ¿Cómo podemos continuar?",
        is_read=False
    )

    # Crear una notificación para el cliente
    notification_message = f"El cliente {quotation.client.user.username} acepto la contraoferta para el trabajo '{quotation.service.name}'."
    Notification.objects.create(
        user=quotation.service.worker.user,  # Enviamos la notificación al cliente que publicó el trabajo
        message=notification_message,
        is_read=False
    ) 

    # Crear una notificación para el cliente
    notification_message = f"El cliente {quotation.client.user.username} ha iniciado un chat contigo'."
    Notification.objects.create(
        user=quotation.service.worker.user,  # Enviamos la notificación al cliente que publicó el trabajo
        message=notification_message,
        is_read=False
    ) 

    messages.success(request, "Cotización aceptada correctamente.")
    return redirect('jobs:list_quotations')


@login_required
def finalize_quotation(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)

    # Asegúrate de que solo el cliente pueda finalizar una cotización
    if request.user != quotation.client.user:
        messages.error(request, "No tienes permisos para finalizar esta cotización.")
        return redirect('jobs:list_quotations')

    # Crear una notificación para el cliente
    notification_message = f"El cliente {quotation.client.user.username} ha finalizado el trabajo '{quotation.service.name}'."
    Notification.objects.create(
        user=quotation.service.worker.user,  # Enviamos la notificación al cliente que publicó el trabajo
        message=notification_message,
        is_read=False
    )

    # Cambiar el estado de is_active a False
    quotation.is_active = False
    quotation.save()
    messages.success(request, "Cotización finalizada correctamente.")
    return redirect('jobs:list_quotations')
