from django.shortcuts import render, redirect
from .models import Carrito, ItemCarrito
from apps.carrito.models import ItemCarrito
from apps.materials.models import Material

from .forms import ItemCarritoForm

def agregar_carrito(request, id):
    producto = Material.objects.get(id=id)
    item_carrito, creado = ItemCarrito.objects.get_or_create(usuario=request.user, producto=producto)
    if creado:
        item_carrito.cantidad = 1
    else:
        item_carrito.cantidad += 1
    if item_carrito.cantidad > producto.stock:
        item_carrito.cantidad = producto.stock
    item_carrito.save()
    producto.stock -= 1
    producto.save()
    return redirect('materials:tienda')

def ver_carrito(request):
    items_carrito = ItemCarrito.objects.filter(usuario=request.user)
    total = sum(item.producto.price * item.cantidad for item in items_carrito)
    return render(request, 'carrito/ver_carrito.html', {'items_carrito': items_carrito, 'total': total})
 
def incrementar_cantidad_producto_carrito(request, id):
    item = ItemCarrito.objects.get(id=id)
    if item.producto.stock > 0:
        item.cantidad += 1
        item.producto.stock -= 1
        item.producto.save()
        item.save()
    else:
        pass
    return redirect('carrito:ver_carrito')

def decrementar_cantidad_producto_carrito(request, id):
    item = ItemCarrito.objects.get(id=id)
    if item.cantidad > 1:
        item.cantidad -= 1
        item.producto.stock += 1
        item.producto.save()
        item.save()
    else:
        item.producto.stock += 1
        item.producto.save()
        item.delete()
    return redirect('carrito:ver_carrito')

def eliminar_producto_carrito(request, id):
    item = ItemCarrito.objects.get(id=id)
    items_carrito = ItemCarrito.objects.filter(usuario=request.user)
    total = sum(item.producto.price * item.cantidad for item in items_carrito)
    if request.method == 'POST':
        producto = item.producto
        producto.stock += item.cantidad  
        producto.save()
        item.delete()
    return redirect('carrito:ver_carrito')
