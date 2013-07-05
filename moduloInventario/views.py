
from django.db.models import Q
from moduloInventario.models import Item, Proveedor, Categoria

from django.core.context_processors import request
from django.shortcuts import render_to_response, render

from django.forms import ModelForm
from django import forms

# Create your views here.

def get_provider(pv_ruc):
    return Proveedor.objects.get(v_ruc__exact=pv_ruc)

def get_providers():
    return Proveedor.objects.all()

def get_providers_by_name(string):
    return Proveedor.objects.filter(v_nombre__icontains=string)

def get_providers_by_social_reason(string):
    return Proveedor.objects.filter(v_razon_social__icontains=string)

def get_category(pv_name):
    return Categoria.objects.get(v_nombre__exact=pv_name)

def get_categories():
    return Categoria.objects.all()

def get_categories_by_name(string):
    return Categoria.objects.get(v_nombre__icontains=string)

def create_item(pv_codigo,pv_nombre,pv_descripcion,pi_cantidad,pf_valor,pv_categoria,pv_proveedor_ruc):
    item = Item(v_codigo=pv_codigo,v_nombre=pv_nombre,v_descripcion=pv_descripcion,i_cantidad=pi_cantidad,f_costo_unitario=pf_valor,b_circulando=True)
    item.categoria = get_category(pv_categoria)
    item.proveedor = get_provider(pv_proveedor_ruc)
    item.save()
    return "Operacion Exitosa. El item se ha creado con exito."

def edit_item(pv_codigo,pv_nombre,pv_descripcion,pi_cantidad,pf_costo,pb_circulando,pv_categoria,pv_proveedor_ruc):
    item = get_item(v_codigo=pv_codigo)
    item.v_nombre = pv_nombre
    item.v_descripcion = pv_descripcion
    item.i_cantidad = pi_cantidad
    item.f_costo_unitario = pf_costo
    if "SI"==pb_circulando:
        item.b_circulando = True
    else:
        item.b_circulando = False
    item.categoria = get_category(pv_categoria)
    item.proveedor = get_provider(pv_proveedor_ruc)
    item.save()
    return 'Operacion Exitosa. La informacion del item ha sido actualizada.'

def get_item(pv_codigo):
    return Item.objects.get(v_codigo__exact=pv_codigo)

def get_items_by_name(string):
    return Item.objects.filter(v_nombre__icontains=string)

def get_items_by_code(string):
    return Item.objects.filter(v_codigo__startswith=string)

def get_items_by_category(string):
    return Item.objects.filter(categoria__v_nombre__exact=string)

def search_items(string,search_type):
    list_item = None
    if None==search_type:
        list_item = Item.objects.all()
    if "name"==search_type:
        list_item = get_items_by_name(string)
    elif "code"==search_type:
        list_item = get_items_by_code(string)
    elif "category"==search_type:
        list_item = get_items_by_category(string)
    return list_item

def delete_item(pv_codigo):
    l_item = get_item(pv_codigo)
    l_item.b_circulando = False
    l_item.save()
    return "Operacion exitosa. Item con cdigo %s eliminado."%(pv_codigo)

def reduce_item(pv_codigo,pv_cantidad):
    l_item = get_item(pv_codigo)
    if 0 == int(l_item.i_cantidad):
        return "No existen unidades con codigo % disponibles."
    elif 0 > int(l_item.i_cantidad) - int(pv_cantidad):
        return "La cantidad de unidades disponibles es menor a las que solicita.\nDisponibles: %s\nSolicita: %s"%(l_item.i_cantidad,pv_cantidad)
    else:
        l_item.i_cantidad = l_item.i_cantidad - int(pv_cantidad)
        l_item.save()
        return "Operacion Exitosa."

def raise_item(pv_codigo,pv_cantidad):
    l_item = get_item(pv_codigo)
    l_item.i_cantidad = l_item.i_cantidad + int(pv_cantidad)
    l_item.save()
    return "Operacion Exitosa."


def inventario(request):
    lista_items = Item.objects.all()
    
    return render_to_response('InventarioFrontEnd/inventario.html',{'lista_items': lista_items})

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

def eliminar_item(request):        
    i = Item.objects.get(pk=(request.GET['q']))
    i.delete()
    return inventario(request)

class InventarioForm(forms.ModelForm):   
    codigo = forms.CharField(required=True,max_length=30)
    nombre = forms.CharField(required=True,max_length=50)
    descripcion = forms.CharField(required=True,max_length=500)
    categoria = forms.ModelChoiceField(queryset=get_categories())
    proveedor = forms.ModelChoiceField(queryset=get_providers())
    costo_unitario = forms.FloatField(required=True)
    cantidad = forms.IntegerField(required=True)
    activo = forms.BooleanField(required=True)
    class Meta:
        model = Item
        
        
