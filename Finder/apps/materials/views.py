from django.shortcuts import render, redirect
from .forms import MaterialForm
from .models import Material

def agregar_material(request):
    if request.method == 'POST':
        print(request.user)
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.empresa = request.user
            material.save()
            return redirect('materials:tienda')  # Redirige a la vista de listar materials
    else:
        form = MaterialForm()
    return render(request, 'materials/agregar_material.html', {'form': form})

def editar_material(request, id):
    material = Material.objects.get(id=id)
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES, instance=material)
        if form.is_valid():
            form.save()
            return redirect('users:empresa_home')
    else:
        form = MaterialForm(instance=material)
    return render(request, 'materials/editar_material.html', {'form': form})

def eliminar_material(request, id):
    material = Material.objects.get(id=id)
    if request.method == 'POST':
        material.delete()
        return redirect('users:empresa_home')
    return render(request, 'materials/eliminar_material.html', {'material': material})

def tienda(request):
    materials = Material.objects.all().order_by('id')
    print(materials)
    return render(request, 'materials/listar_materials.html',{'materials': materials})