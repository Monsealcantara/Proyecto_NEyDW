# apps/jobs/views.py
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import JobCreateForm
from .models import Job, Quotation

def job_list(request):
    jobs = Job.objects.filter(is_active=True)
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'jobs/job_detail.html', {'job': job})

@login_required
def create_job(request):
    """Vista para crear un nuevo trabajo por parte de un cliente."""
    if request.method == 'POST':
        form = JobCreateForm(request.POST)
        if form.is_valid():
            # Asignamos el cliente que está creando el trabajo
            job = form.save(commit=False)
            job.client = request.user.client_profile  # Asociamos el trabajo al perfil del cliente
            job.save()
            return redirect('jobs:job_list')  # Redirige a la lista de trabajos
    else:
        form = JobCreateForm()

    return render(request, 'jobs/create_job.html', {'form': form})


def quotation_detail(request, quotation_id):
    """Vista para ver los detalles de una cotización."""
    # Obtenemos la cotización de la base de datos
    quotation = get_object_or_404(Quotation, id=quotation_id)

    # Verificamos si el usuario actual es el trabajador que hizo la cotización
    is_owner = quotation.worker.user == request.user

    # Si es el cliente, mostramos información del trabajo
    is_client = quotation.job.client.user == request.user

    return render(request, 'jobs/quotation_detail.html', {
        'quotation': quotation,
        'is_owner': is_owner,
        'is_client': is_client,
    })

@login_required
def accept_or_reject_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            job.status = 'accepted'
            job.save()
            messages.success(request, 'Trabajo aceptado exitosamente.')
        elif action == 'reject':
            job.status = 'rejected'
            job.save()
            messages.success(request, 'Trabajo rechazado exitosamente.')

        return redirect('job_list')  # Redirige a la lista de trabajos u otra página
    return render(request, 'jobs/accept_reject_job.html', {'job': job})
