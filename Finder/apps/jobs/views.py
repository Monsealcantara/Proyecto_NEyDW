# apps/jobs/views.py
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import QuotationForm, CounterOfferForm, EditQuotationForm
from .models import  Quotation, Review
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
    # Agregar un campo extra 'review_status' para cada cotización, indicando el estado de la reseña
    for quotation in quotations:
        # Verificar si existe una reseña para esta cotización
        review = Review.objects.filter(quotation=quotation).first()
        if review:  # Si existe una reseña
            if review.rating is None:  # Si la reseña existe pero no tiene calificación
                quotation.review_status = 'pending'  # En espera de calificación
            else:
                quotation.review_status = 'reviewed'  # Ya ha sido calificada
        else:
            quotation.review_status = 'not_available'  # No disponible
    return render(request, 'jobs/job_list.html', {'quotations': quotations})

@login_required
def list_quotations(request):
    client = Client.objects.get(user=request.user)
    quotations = Quotation.objects.filter(client=client)
    # Agregar un campo extra 'review_status' para cada cotización, indicando el estado de la reseña
    for quotation in quotations:
        # Verificar si existe una reseña para esta cotización
        review = Review.objects.filter(quotation=quotation).first()
        if review:  # Si existe una reseña
            if review.rating is None:  # Si la reseña existe pero no tiene calificación
                quotation.review_status = 'pending'  # Pendiente de calificación
            else:
                quotation.review_status = 'reviewed'  # Ya ha sido calificada
                quotation.review = review  # Pasar la reseña completa (calificación y comentario)
        else:
            quotation.review_status = 'not_available'  # No disponible
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
    chat.quotation=quotation
    chat.save()

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
    chat.quotation=quotation
    chat.save()

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
    # Cambiar el estado de is_active a False
    quotation.is_active = False
    quotation.save()

    # Si existe un chat relacionado con la cotización, lo desactivamos
    chat = Chat.objects.filter(quotation=quotation).first()
    if chat:
        chat.is_activate = False
        chat.save()

    # Crear una notificación para el cliente
    notification_message = f"El cliente {quotation.client.user.username} ha finalizado el chat '{quotation.service.name}'."
    Notification.objects.create(
        user=quotation.service.worker.user,  # Enviamos la notificación al cliente que publicó el trabajo
        message=notification_message,
        is_read=False
    )
    
    Review.objects.create(
            quotation=quotation,
            worker=quotation.service.worker,
            client=quotation.client,
            rating=None,  # Aquí no estamos asignando un rating todavía
            comment=None,  # Deja el comentario vacío inicialmente
            status=True
        )

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

    messages.success(request, "Cotización finalizada correctamente.")
    return redirect('jobs:list_quotations')

@login_required
def leave_review(request, pk):
    # Obtener la cotización que se está reseñando
    quotation = get_object_or_404(Quotation, pk=pk)
    # Asegurarse de que solo el cliente pueda dejar una reseña
    if request.user != quotation.client.user:
        messages.error(request, "No tienes permisos para dejar una reseña.")
        return redirect('jobs:list_quotations')
    # Verificar si ya existe una reseña para esta cotización
    review = Review.objects.filter(quotation=quotation).first()
    if review:  # Si ya existe la reseña, actualizamos
        if request.method == 'POST':
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')
            # Validar la calificación
            if rating and comment:
                try:
                    rating = int(rating)
                    if rating < 1 or rating > 5:
                        raise ValueError("La calificación debe estar entre 1 y 5.")
                except ValueError:
                    messages.error(request, "La calificación debe ser un número entre 1 y 5.")
                    return redirect('jobs:leave_review', pk=quotation.pk)
                # Actualizar la reseña
                review.rating = rating
                review.status = False
                review.comment = comment
                review.save()

                 # Actualizar la calificación del trabajador, solo si la reseña no estaba calificada
                if review.status == False:
                    # Obtener todas las reseñas del trabajador
                    worker_reviews = Review.objects.filter(worker=quotation.service.worker)

                    # Calcular el promedio de las calificaciones
                    total_rating = sum([rev.rating for rev in worker_reviews])
                    average_rating = total_rating / len(worker_reviews) if worker_reviews else 0

                    # Actualizar la calificación del trabajador
                    worker = quotation.service.worker
                    worker.rating = round(average_rating, 2)
                    worker.save()
                    
                # Notificar al trabajador sobre la actualización de la reseña
                notification_message = f"El cliente {quotation.client.user.username} ha reseñado el trabajo '{quotation.service.name}'."
                Notification.objects.create(
                    user=quotation.service.worker.user,
                    message=notification_message,
                    is_read=False
                )
                messages.success(request, "Reseña actualizada correctamente.")
                return redirect('jobs:list_quotations')
    # Si el GET, mostramos el formulario para dejar o actualizar la reseña
    return render(request, 'jobs/leave_review.html', {'quotation': quotation, 'review': review})
