# apps/jobs/views.py
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import QuotationForm, CounterOfferForm, EditQuotationForm
from .models import  Quotation
from apps.users.models import Service, User, Client

@login_required
def create_quotation(request, service_id):
    # Obtienes el servicio con el ID proporcionado
    service = Service.objects.get(id=service_id)

    if request.method == 'POST':
        form = QuotationForm(request.POST)
        if form.is_valid():
            # Creas la cotización sin guardar (commit=False)
            quotation = form.save(commit=False)
            # Asignas el cliente relacionado con el usuario actual
            quotation.client = Client.objects.get(user=request.user)
            quotation.service = service  # El servicio asociado
            quotation.save()  # Guardas la cotización
            return redirect('jobs:list_quotations')  # Redirigir al cliente a una lista de sus cotizaciones

    else:
        form = QuotationForm()

    return render(request, 'jobs/create_quotation.html', {'form': form, 'service': service})


@login_required
def edit_quotation(request, pk):
    # Obtener la cotización a editar
    quotation = get_object_or_404(Quotation, pk=pk)
    
    # Verifica si el usuario autenticado es el trabajador asociado a la cotización
    if request.user != quotation.client.user:
        # Si no es el trabajador, redirige a la lista de cotizaciones
        return redirect('jobs:list_quotations')

    # Si el usuario es un cliente, asignamos el cliente en caso de que se modifique
    if request.user.role == 'cliente' and not quotation.client:
        # Suponiendo que el cliente no se ha asignado correctamente, asignamos el cliente
        quotation.client = Client.objects.get(user=request.user)
    
    if request.method == 'POST':
        # Creamos el formulario con los datos actuales de la cotización
        form = EditQuotationForm(request.POST, instance=quotation)
        if form.is_valid():
            # Guardamos los cambios en la cotización
            form.save()
            return redirect('jobs:quotation_detail', pk=quotation.pk)
    else:
        # Si es un GET, mostramos el formulario con la información de la cotización
        form = EditQuotationForm(instance=quotation)
    
    # Renderizamos la plantilla con el formulario
    return render(request, 'jobs/edit_quotation.html', {'form': form})
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

# @login_required
# def counter_offer_quotation(request, quotation_id):
#     quotation = Quotation.objects.get(id=quotation_id)

#     # Solo el trabajador asociado a esta cotización puede hacer una contraoferta
#     if request.user != quotation.worker.user:
#         return redirect('users:profile')  # Redirigir si el trabajador no tiene permiso

#     if request.method == 'POST':
#         # Aquí puedes permitir que el trabajador ingrese su contraoferta (nuevo precio y tiempo estimado)
#         new_price = request.POST['price']
#         new_time_estimate = request.POST['time_estimate']

#         # Actualizar la cotización con la contraoferta
#         quotation.counter_offer = new_price
#         quotation.counter_offer_accepted = False  # Marcar como pendiente de aceptación
#         quotation.time_estimate = new_time_estimate
#         quotation.save()

#         return redirect('jobs:list_services')

#     return render(request, 'users/counter_offer_quotation.html', {'quotation': quotation})


# @login_required
# def accept_counter_offer(request, quotation_id):
#     quotation = Quotation.objects.get(id=quotation_id)

#     # Solo el cliente asociado a esta cotización puede aceptarla
#     if request.user != quotation.worker.user:
#         return redirect('users:profile')

#     if request.method == 'POST':
#         if 'accept' in request.POST:
#             quotation.counter_offer_accepted = True  # El cliente acepta la contraoferta
#         elif 'reject' in request.POST:
#             quotation.counter_offer_accepted = False  # El cliente rechaza la contraoferta

#         quotation.save()

#         return redirect('users:list_services')  # Redirigir al cliente

#     return render(request, 'jobs/accept_counter_offer.html', {'quotation': quotation})
