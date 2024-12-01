from django.shortcuts import render, redirect
from .models import Venta, ItemVenta
from django.utils import timezone
from apps.carrito.models import ItemCarrito

def realizar_compra(request):
    items_carrito = ItemCarrito.objects.filter(usuario=request.user)
    venta = Venta.objects.create(usuario=request.user, fecha_venta=timezone.now())
    for item in items_carrito:
        item_venta = ItemVenta.objects.create(
            producto=item.producto, 
            cantidad=item.cantidad, 
            precio=item.producto.price
        )
        venta.items.add(item_venta)
        item.producto.save()
        item.delete()
    return redirect('venta:compra_exitosa')
    
def compra_exitosa(request):
    return render(request, 'venta/compra_exitosa.html')

def ventas_list(request):
    ventas = Venta.objects.filter(items__producto__empresa=request.user).distinct().prefetch_related('items')
    return render(request, 'venta/ventas_list.html', {'ventas': ventas})

def compras_lista(request):
    ventas = Venta.objects.filter(usuario=request.user).prefetch_related('items')
    
    for venta in ventas:
        venta.total = sum(item.cantidad * item.precio for item in venta.items.all())

    return render(request, 'venta/compras_lista.html', {'ventas': ventas})
