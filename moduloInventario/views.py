
from django.db.models import Q
from moduloInventario.models import Item
from django.shortcuts import render_to_response, render
from django import forms
from django.contrib.auth.decorators import login_required


def inventario(request):
    lista_items = Item.objects.all()
    usuario = request.user
    return render_to_response('InventarioFrontEnd/inventario.html',{'lista_items': lista_items, 'user': usuario})

def nuevo_item(request):
    if request.method == 'POST':
        form = InventarioForm(request.POST)
        
        if form.is_valid():
            i = Item(codigo=request.POST['codigo'],nombre=request.POST['nombre'],descripcion=request.POST['descripcion'],proveedor=request.POST['proveedor'],costo_unitario=request.POST['costo_unitario'],cantidad=request.POST['cantidad'])
            i.save()
            return inventario(request)
    else:
        if request.method != 'POST':
            form = InventarioForm()
    return render(request, 'InventarioFrontEnd/nuevoItem.html', {'form': form})

def editar_item(request):        
    i = Item.objects.get(pk=(request.GET['q']))
    
    if request.method != 'POST':
        form = InventarioForm(instance=i)
        form.id = request.GET['q']
        if form.is_valid():
            form.save()
    else:
        if request.method == 'POST':
            form = InventarioForm(request.POST)
            if form.is_valid():
                i.codigo = request.POST['codigo']
                i.nombre = request.POST['nombre']
                i.descripcion = request.POST['descripcion']
                i.proveedor = request.POST['proveedor']
                i.costo_unitario = request.POST['costo_unitario']
                i.cantidad = request.POST['cantidad']
                i.save()
                return inventario(request)
    return render(request, 'InventarioFrontEnd/nuevoItem.html', {'form': form})

@login_required
def eliminar_item(request):        
    i = Item.objects.get(pk=(request.GET['q']))
    i.delete()
    return inventario(request)

class InventarioForm(forms.ModelForm):   
    codigo = forms.CharField(required=True,max_length=30)
    nombre = forms.CharField(required=True,max_length=50)
    descripcion = forms.CharField(required=True,max_length=500)
    proveedor = forms.CharField(required=False,max_length=30)
    costo_unitario = forms.FloatField(required=True)
    cantidad = forms.FloatField(required=True)
    
    class Meta:
        model = Item
        
