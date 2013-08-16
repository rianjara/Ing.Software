from moduloInventario.models import Item, Proveedor, Categoria
from django.shortcuts import render_to_response, render
from django import forms
from django.contrib.auth.decorators import login_required

# Create your views here.

def get_provider(pv_id):
    try:
        return Proveedor.objects.get(id=pv_id)
    except:
        return None

def get_provider_by_social_reason(string):
    return Proveedor.objects.filter(razon_social=string)

def get_providers():
    return Proveedor.objects.all()

def get_providers_by_name(string):
    return Proveedor.objects.filter(nombre__icontains=string)

def get_providers_by_social_reason(string):
    return Proveedor.objects.filter(razon_social__icontains=string)

def new_provider(pv_nombre,pv_razon_social,pv_ruc,pv_telefono):
    if pv_nombre is None:
        return "Operacion Fallida. El campo de el nombre esta vacio."
    elif pv_razon_social is None:
        return "Operacion Fallida. El campo de la razon social esta vacio."
    elif pv_ruc is None:
        return "Operacion Fallida. El campo de el ruc esta vacio."
    elif pv_telefono is None:
        return "Operacion Fallida. El campo de el telefono esta vacio."
    elif None != get_provider_by_social_reason(pv_razon_social):
        return "Operacion Fallida. Ya existe un proveedor con la misma razon social."
    else:
        provider = Proveedor(nombre=pv_nombre,razon_social=pv_razon_social,ruc=pv_ruc,telefono=pv_telefono)
        provider.save()
        return "Operacion Exitosa. El proveedor ha sido ingresado en la base de datos."
    
def update_provider(proveedor,pv_nombre,pv_razon_social,pv_ruc,pv_telefono):
    tmp = get_provider_by_social_reason(pv_razon_social)
    if tmp != None:
        if tmp.id != proveedor.id:
            return "Operacion Fallida. No puede asignar una razon social que ya esta siendo usado por otro proveedor."
    proveedor.nombre = pv_nombre
    proveedor.razon_social = pv_razon_social
    proveedor.ruc = pv_ruc
    proveedor.telefono = pv_telefono
    proveedor.save()
    return "Operacion Exitosa. Los datos del proveedor han sido actualizados."

def edit_provider(p_id, pv_nombre,pv_razon_social,pv_ruc,pv_telefono):
    if pv_nombre is None:
        return "Operacion Fallida. El campo de el nombre esta vacio."
    elif pv_razon_social is None:
        return "Operacion Fallida. El campo de la razon social esta vacio."
    elif pv_ruc is None:
        return "Operacion Fallida. El campo de el ruc esta vacio."
    elif pv_telefono is None:
        return "Operacion Fallida. El campo de el telefono esta vacio."
    else:
        proveedor = get_provider(p_id)
        if proveedor is None:
            return "Opercion Fallida. El proveedor cuyos datos desea modificar, no esta regitrado en la base de datos."
        else:
            return update_provider(proveedor, pv_nombre, pv_razon_social, pv_ruc, pv_telefono)

def get_category(pv_id):
    return Categoria.objects.get(id=pv_id)

def get_category_by_name(pv_nombre):
    return Categoria.objects.get(nombre=pv_nombre)

def get_categories():
    return Categoria.objects.all()

def get_categories_by_name(string):
    return Categoria.objects.get(nombre__icontains=string)

def new_category(pv_nombre,pv_descripcion):
    if pv_nombre is None:
        return "Operacion Fallida. El campo de el nombre esta vacio."
    elif None != get_category_by_name(pv_nombre):
        return "Operacion Fallida. Ya existe una categoria con el mismo nombre."
    else:
        category = Categoria(nombre=pv_nombre,descripcion=pv_descripcion)
        category.save()
        return "Operacion Exitosa. La categoria ha sido ingresada en la base de datos."
    
def update_category(categoria,p_nombre,p_descripcion):
    tmp = get_category_by_name(p_nombre)
    if tmp != None:
        if tmp.id != categoria.id:
            return "Operacion Fallida. No puede asignar un nombre que ya esta siendo usado por otra categoria."
    categoria.nombre = p_nombre
    categoria.descripcion = p_descripcion
    categoria.save()
    return "Operacion Exitosa. Los datos de la categoria han sido actualizados."

def edit_category(p_id, pv_nombre,pv_descripcion):
    if pv_nombre is None:
        return "Operacion Fallida. El campo de el nombre esta vacio."
    else:
        category = get_category(p_id)
        if category is None:
            return "Operacion Fallida. La categoria cuyos datos desea modificar, no esta registrada en la base de datos"
        else:
            return update_category(category, pv_nombre, pv_descripcion)

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
        
class ProveedorForm(forms.ModelForm):   
    nombre = forms.CharField(required=True,max_length=200)
    descripcion = forms.CharField(required=False,max_length=200)
    ruc = forms.CharField(required=True,max_length=20)
    telefono = forms.CharField(required=False,max_length=10)
    class Meta:
        model = Proveedor

class CategoriaForm(forms.ModelForm):   
    nombre = forms.CharField(required=True,max_length=100)
    descripcion = forms.CharField(required=False,max_length=2000)
    class Meta:
        model = Categoria