# apps/jobs/views.py
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import JobCreateForm
from .models import Job

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
            return redirect('jobs:job_list')  # Redirige a la lista de trabajos (o a donde quieras)
    else:
        form = JobCreateForm()

    return render(request, 'jobs/create_job.html', {'form': form})
