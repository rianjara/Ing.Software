
from django.db.models import Q
#from django.contrib.auth import authenticate
from django.template import RequestContext
from moduloInventario.models import Item, Proveedor, Categoria, Orden_Compra, Detalle_Orden_Compra
from django.shortcuts import render_to_response, render
from django import forms
from django.http.response import HttpResponse

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

def get_item(pv_id):
    return Item.objects.get(id=pv_id)

def get_item_by_code(pv_codigo):
    return Item.objects.get(codigo=pv_codigo)

def get_items_by_string(string,boolean):
    return Item.objects.filter(Q(codigo__startswith=string) | Q(nombre__icontains=string) | Q(categoria__nombre__startswith=string) | Q(proveedor__razon_social__startswith=string))

def get_items_by_name(string,boolean):
    return Item.objects.filter(nombre__icontains=string)

def get_items_by_code(string,boolean):
    return Item.objects.filter(codigo__startswith=string)

def get_items_by_category(string,boolean):
    return Item.objects.filter(categoria__nombre__exact=string)

def search_items(string,search_type):
    list_item = None
    if None==string:
        list_item = Item.objects.all()
    elif "name"==search_type:
        list_item = get_items_by_name(string)
    elif "code"==search_type:
        list_item = get_items_by_code(string)
    elif "category"==search_type:
        list_item = get_items_by_category(string)
    else:
        list_item = get_items_by_string(string)
    return list_item
        
def create_item(pv_codigo,pv_nombre,pv_descripcion,pf_valor_venta,pv_categoria):
    if pv_codigo is None:
        return "Operacion Fallida. El campo de el codigo esta vacio."
    elif pv_nombre is None:
        return "Operacion Fallida. El campo de el nombre esta vacio."
    elif pf_valor_venta is None:
        return "Operacion Fallida. El campo de el valor de venta esta vacio."
    elif pv_categoria is None:
        return "Operacion Fallida. El campo de la categoria esta vacio."
    else:
        try:
            item = get_item_by_code(pv_codigo)
            return "Operacion Fallida. Ya existe un item con el mismo codigo."
        except:
            item = Item(codigo=pv_codigo,nombre=pv_nombre,descripcion=pv_descripcion,cantidad=0,valor_venta=pf_valor_venta)
            item.categoria = get_category(pv_categoria)
            item.save()
            return "Operacion Exitosa. El item se ha creado con exito."
    
def update_item(item,p_codigo,p_nombre,p_descripcion,p_categoria,p_valor):
    tmp = get_item_by_code(p_codigo)
    if tmp != None:
        if tmp.id != item.id:
            return "Operacion Fallida. No puede asignar un codigo que ya esta siendo usado por otro item."
    item.codigo = p_codigo
    item.nombre = p_nombre
    item.descripcion = p_descripcion
    item.valor_venta = p_valor
    item.categoria = get_category(p_categoria)
    item.save()
    return "Operacion Exitosa. Los datos del item han sido actualizados."
   
def edit_item(p_id,pv_codigo,pv_nombre,pv_descripcion,pf_valor_venta,pv_categoria):
    if pv_codigo is None:
        return "Operacion Fallida. El campo de el codigo esta vacio."
    elif pv_nombre is None:
        return "Operacion Fallida. El campo de el nombre esta vacio."
    elif pf_valor_venta is None:
        return "Operacion Fallida. El campo de el valor de venta esta vacio."
    elif pv_categoria is None:
        return "Operacion Fallida. El campo de la categoria esta vacio."
    elif type(pf_valor_venta) != float:
        return "Operacion Fallida. El campo valor venta no corresponde al tipo de dato flotante"
    else:
        item = get_item(p_id)
        if item is None:
            return "Operacion Fallida. El item que desea modificar no existe en la base de datos."
        else:
            return update_item(item, pv_codigo, pv_nombre, pv_descripcion, pv_categoria, pf_valor_venta)

def inventario(request):
    """
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)
    else:
    """
    if not request.GET.__contains__("string_search"):
        return render_to_response('InventarioFrontEnd/inventario.html',{'lista_items': search_items(None,None)})
    else:
        return render_to_response('InventarioFrontEnd/inventario.html',{'lista_items': search_items(request.GET['string_search'],None),'string_busqueda':request.GET['string_search']})

def nuevo_item(request):
    """
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)
    else:
    """
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            mensaje = create_item(request.POST['codigo'], request.POST['nombre'], request.POST['descripcion'], request.POST['valor_venta'], request.POST['categoria'])
            if mensaje.startswith("Operacion Exitosa."):
                return render_to_response('InventarioFrontEnd/inventario.html',{'lista_items': search_items(None,None),'mensaje':mensaje})
            else:
                return render_to_response('InventarioFrontEnd/item.html', {'form': form,'mensaje':mensaje},context_instance=RequestContext(request))
        else:
            return render_to_response('InventarioFrontEnd/item.html', {'form': form,'mensaje':form.errors},context_instance=RequestContext(request))
    else:
        form = ItemForm()
        return render_to_response('InventarioFrontEnd/item.html', {'form': form,'editing': False},context_instance=RequestContext(request))

def editar_item(request):        
    i = Item.objects.get(pk=(request.GET['q']))
    if request.method != 'POST':
        form = ItemForm(instance=i)
        form.id = request.GET['q']
        if form.is_valid():
            form.save()
    else:
        if request.method == 'POST':
            form = ItemForm(request.POST)
            mensaje = edit_item(request.POST['codigo'], request.POST['nombre'], request.POST['valor_venta'], request.POST['descripcion'], request.POST['categoria'])
            return render_to_response('InventarioFrontEnd/inventario.html',{'lista_items': search_items(None,None),'mensaje':mensaje})
    return render(request, 'InventarioFrontEnd/item.html', {'form': form,'editing': True})

class ItemForm(forms.ModelForm):   
    codigo = forms.CharField(required=True,max_length=30)
    nombre = forms.CharField(required=True,max_length=100)
    descripcion = forms.CharField(required=False,max_length=2000)
    categoria = forms.ModelChoiceField(queryset=get_categories())
    cantidad = forms.IntegerField(required=False,initial=0)
    valor_venta = forms.FloatField(required=True)
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

        
