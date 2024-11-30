# apps/users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from .forms import ProfileFormWorker, ProfileFormClient
from .models import User, Worker, Client


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('users:profile')
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)  # Finaliza la sesión del usuario
    return redirect('users:login') 

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']  # Captura el correo electrónico
        role = request.POST['role']

        # Verifica si el usuario ya existe
        if User.objects.filter(username=username).exists():
            return render(request, 'users/register.html', {'error': 'El usuario ya existe.'})

        # Crea el usuario base
        try:
            user = User.objects.create_user(username=username, password=password, email=email, role=role)

            # Asigna el perfil según el rol
            if role == 'cliente':
                if Client.objects.filter(user=user).exists():
                    return render(request, 'users/register.html', {'error': 'Este usuario ya está registrado como cliente.'})
                Client.objects.create(user=user)

            elif role == 'trabajador':
                if Worker.objects.filter(user=user).exists():
                    return render(request, 'users/register.html', {'error': 'Este usuario ya está registrado como trabajador.'})
                Worker.objects.create(user=user)

            login(request, user)
            return redirect('users:profile')
        except IntegrityError:
            return render(request, 'users/register.html', {'error': 'Ocurrió un error al registrar al usuario.'})

    return render(request, 'users/register.html')

def profile_view(request):
    #Implementacion de los datos de perfil del cliente

    #Implementacion de los datos de perfil del trabajador
    return render(request, 'users/profile.html', {'user': request.user})
@login_required
def edit_profile_view(request):
    # Determinamos si el usuario es trabajador o cliente
    if hasattr(request.user, 'worker_profile'):  # Es un trabajador
        profile = request.user.worker_profile
        form = ProfileFormWorker(instance=profile)
        form_class = ProfileFormWorker
    else:  # Es un cliente
        profile, created = Client.objects.get_or_create(user=request.user)
        form = ProfileFormClient(instance=profile)
        form_class = ProfileFormClient

    if request.method == 'POST':
        form = form_class(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
            return redirect('users:profile')  # Redirigir a la página de perfil
    return render(request, 'users/edit_profile.html', {'form': form})
