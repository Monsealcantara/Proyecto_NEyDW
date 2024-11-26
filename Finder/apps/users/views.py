# apps/users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
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
    return render(request, 'users/profile.html', {'user': request.user})
