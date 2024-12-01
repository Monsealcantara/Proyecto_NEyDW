# apps/users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from .forms import ProfileFormWorker, ProfileFormClient, UserEditForm, ServiceForm
from .models import User, Worker, Client, Service, WorkerService, Keyword

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Si las credenciales son correctas, inicia la sesión
            login(request, user)
            
            # Verificar el rol del usuario y redirigir según el tipo
            if user.role == 'cliente':
                return redirect('users:client_home')  # Redirige a la vista de cliente
            elif user.role == 'trabajador':
                return redirect('users:worker_home')  # Redirige a la vista de trabajador
            else:
                # Si no tiene un rol asignado (opcional, pero recomendable tenerlo manejado)
                messages.error(request, 'No se ha asignado un rol al usuario.')
                return redirect('login')
        else:
            messages.error(request, 'Credenciales incorrectas.')
            return redirect('login')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)  # Finaliza la sesión del usuario
    return redirect('login') 

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

            return redirect('login')
        except IntegrityError:
            return render(request, 'users/register.html', {'error': 'Ocurrió un error al registrar al usuario.'})
    return render(request, 'users/register.html')

@login_required
def worker_home(request):
    return render(request, 'users/home_empleado.html')

@login_required
def client_home(request):
    return render(request, 'users/home_cliente.html')

@login_required
def profile_view(request):
    #Implementacion de los datos de perfil del cliente

    #Implementacion de los datos de perfil del trabajador
    return render(request, 'users/profile.html', {'user': request.user})
    
@login_required
def edit_profile_view(request):
    # Determinamos si el usuario es trabajador o cliente
    if hasattr(request.user, 'worker_profile'):  # Es un trabajador
        profile = request.user.worker_profile
        form_profile = ProfileFormWorker(instance=profile)
        form_class = ProfileFormWorker
    else:  # Es un cliente
        profile, created = Client.objects.get_or_create(user=request.user)
        form_profile = ProfileFormClient(instance=profile)
        form_class = ProfileFormClient

    # Formulario para editar los datos del usuario
    form_user = UserEditForm(instance=request.user)

    if request.method == 'POST':
        form_user = UserEditForm(request.POST, instance=request.user)
        form_profile = form_class(request.POST, instance=profile)

        if form_user.is_valid() and form_profile.is_valid():
            form_user.save()  # Guarda los datos del usuario
            form_profile.save()  # Guarda los datos adicionales del perfil
            return redirect('users:profile')  # Redirige a la página de perfil después de guardar

    return render(request, 'users/edit_profile.html', {
        'form_user': form_user,
        'form_profile': form_profile
    })

# Vista para listar los servicios ofrecidos por el trabajador
@login_required
def list_services(request):
    services = Service.objects.filter(worker=request.user.worker_profile)  # Solo los servicios del trabajador actual
    print(services)
    return render(request, 'users/list_services.html', {'services': services})  # Pasar 'services' y no 'users'

@login_required
def create_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        
        if form.is_valid():
            # Guardar el servicio primero
            service = form.save(commit=False)
            service.worker = request.user.worker_profile  # Asegúrate de asociar el trabajador
            service.save()  # Guarda el servicio
            
            # Asociar las palabras clave existentes
            keywords = form.cleaned_data['keywords']
            service.keywords.set(keywords)  # Asocia las palabras clave existentes
            
            # Crear nuevas palabras clave si el usuario las ha ingresado
            new_keywords = form.cleaned_data['new_keywords']
            if new_keywords:
                # Si el trabajador ha ingresado nuevas palabras clave
                new_keyword = Keyword.objects.create(word=new_keywords)
                service.keywords.add(new_keyword)  # Asocia la nueva palabra clave

            messages.success(request, 'Servicio creado exitosamente.')
            return redirect('users:list_services')  # Redirige a la lista de servicios

    else:
        form = ServiceForm()
    
    return render(request, 'users/create_service.html', {'form': form})

    # Aseguramos que el usuario autenticado es un trabajador
    try:
        worker = Worker.objects.get(user=request.user)
    except Worker.DoesNotExist:
        # Si el usuario no es un trabajador, mostrar un mensaje de error
        messages.error(request, "Debes ser un trabajador para crear un servicio.")
        return redirect('some-error-page')  # Redirige a una página de error o a donde lo consideres adecuado

    if request.method == 'POST':
        form = ServiceForm(request.POST)
        
        if form.is_valid():
            # Guardar el servicio, pero sin guardar la relación 'worker'
            service = form.save(commit=False)
            
            # Asignamos al trabajador actual al servicio
            service.worker = worker
            service.save()  # Guardamos el servicio
            
            # Asociar las palabras clave existentes
            keywords = form.cleaned_data['keywords']
            service.keywords.set(keywords)  # Asociamos las palabras clave existentes
            
            # Agregar nuevas palabras clave
            new_keywords = form.cleaned_data['new_keywords']
            if new_keywords:
                # Si el trabajador ha ingresado nuevas palabras clave, las agregamos
                keyword, created = Keyword.objects.get_or_create(name=new_keywords)
                service.keywords.add(keyword)  # Agregar la nueva palabra clave al servicio
                
            service.save()  # Guardar cambios finales en el servicio
            messages.success(request, "Servicio creado exitosamente.")
            return redirect('some-success-page')  # Redirige a la página de éxito o donde lo desees
    
    else:
        form = ServiceForm()
    
    return render(request, 'users:create_service.html', {'form': form})

# Vista para editar un servicio existente
@login_required
def edit_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.user != service.worker.user:
        return redirect('users:list_services')  # Si no es el trabajador, redirige

    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('users:list_services')
    else:
        form = ServiceForm(instance=service)
    
    return render(request, 'users/edit_service.html', {'form': form})

# Vista para eliminar un servicio
@login_required
def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.user != service.worker.user:
        return redirect('users:list_services')  # Si no es el trabajador, redirige
    
    if request.method == 'POST':
        service.delete()
        return redirect('users:list_services')

    return render(request, 'users/delete_service.html', {'users': service})
