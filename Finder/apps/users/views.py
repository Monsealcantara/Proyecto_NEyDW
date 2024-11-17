# apps/users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import User

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('users:profile')
    return render(request, 'users/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']
        user = User.objects.create_user(username=username, password=password, role=role)
        login(request, user)
        return redirect('users:profile')
    return render(request, 'users/register.html')

def profile_view(request):
    return render(request, 'users/profile.html', {'user': request.user})
