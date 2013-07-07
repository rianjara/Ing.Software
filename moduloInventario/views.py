
from django.db.models import Q
from moduloInventario.models import Item, Proveedor, Categoria

from django.core.context_processors import request
from django.shortcuts import render_to_response, render
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm
from django import forms
from django.db.utils import IntegrityError
from django.http.response import HttpResponseRedirect, HttpResponse

# Create your views here.

def get_provider(pv_id):
    try:
        return Proveedor.objects.get(id=pv_id)
    except:
        return None

def get_providers():
    return Proveedor.objects.all()

def get_providers_by_name(string):
    return Proveedor.objects.filter(nombre__icontains=string)

def get_providers_by_social_reason(string):
    return Proveedor.objects.filter(razon_social__icontains=string)

def get_category(pv_id):
    return Categoria.objects.get(id=pv_id)

def get_categories():
    return Categoria.objects.all()

def get_categories_by_name(string):
    return Categoria.objects.get(nombre__icontains=string)

def create_item(pv_codigo,pv_nombre,pv_descripcion,pi_cantidad,pf_valor,pv_categoria,pv_proveedor):
        try:
            item = Item(codigo=pv_codigo,nombre=pv_nombre,descripcion=pv_descripcion,cantidad=pi_cantidad,costo_unitario=pf_valor,circulando=True)
            item.categoria = get_category(pv_categoria)
            item.proveedor = get_provider(pv_proveedor)
            item.save()
        except IntegrityError,e:
            return "Operacion Fallida. %s"%("Ya existe item con dicho codigo."if e.args[0].endswith('unique') else 'Algun campo requerido se ha enviado vacio.')
        except ObjectDoesNotExist,e:
            return "Operacion Fallida. %s no existe."%("Categoria"if e.args[0].startswith('Categoria') else 'Proveedor')
        except ValueError:
            return "Operacion Fallida. En algun campo se esta enviando un tipo de dato incorrecto."
        else:
            if None==item.id:
                return "Operacion Fallida. El item no se ha podido insertar en la base."
            else:
                return "Operacion Exitosa. El item se ha creado con exito."
        

def edit_item(pv_codigo,pv_nombre,pv_descripcion,pi_cantidad,pf_costo,pb_circulando,pv_categoria,pv_proveedor):
    item = get_item_by_code(pv_codigo)
    item.codigo = pv_codigo
    item.nombre = pv_nombre
    item.descripcion = pv_descripcion
    item.cantidad = pi_cantidad
    item.costo_unitario = pf_costo
    item.circulando = pb_circulando
    """if "SI"==pb_circulando:
        item.b_circulando = True
    else:
        item.b_circulando = False"""
    item.categoria = get_category(pv_categoria)
    item.proveedor = get_provider(pv_proveedor)
    item.save()
    return 'Operacion Exitosa. La informacion del item ha sido actualizada.'

def get_item(pv_id):
    return Item.objects.get(id=pv_id)

def get_item_by_code(pv_codigo):
    return Item.objects.get(codigo=pv_codigo)

def get_items_by_name(string,boolean):
    return Item.objects.filter(nombre__icontains=string,circulando=True)if boolean else Item.objects.filter(nombre__icontains=string)

def get_items_by_code(string,boolean):
    return Item.objects.filter(codigo__startswith=string,circulando=True)if boolean else Item.objects.filter(codigo__startswith=string)

def get_items_by_category(string,boolean):
    return Item.objects.filter(categoria__nombre__exact=string,circulando=True)if boolean else Item.objects.filter(categoria__nombre__exact=string)

def search_items(string,search_type,boolean):
    list_item = None
    if None==search_type:
        list_item = Item.objects.filter(circulando=True) if boolean else Item.objects.all()
    if "name"==search_type:
        list_item = get_items_by_name(string,boolean)
    elif "code"==search_type:
        list_item = get_items_by_code(string,boolean)
    elif "category"==search_type:
        list_item = get_items_by_category(string,boolean)
    return list_item

def delete_item(pv_id):
    l_item = get_item(pv_id)
    if None != l_item:
        if l_item.circulando:
            l_item.circulando = False
            l_item.save()
            print(l_item.circulando)
            return "Operacion exitosa. Item %s eliminado."%(l_item.nombre)
        else:
            return "Operacion fallida. Item ya esta inactivo."
    else:
        return "Operacion fallida. Item no existe."

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
    return render_to_response('InventarioFrontEnd/inventario.html',{'lista_items': search_items(None,None,False)})

def nuevo_item(request):
    if request.method == 'POST':
        form = InventarioForm(request.POST)
        if form.is_valid():
            print(request.POST['categoria'])
            mensaje = create_item(request.POST['codigo'], request.POST['nombre'], request.POST['descripcion'], request.POST['cantidad'], request.POST['costo_unitario'], request.POST['categoria'], request.POST['proveedor'])
            if mensaje.startswith("Operacion Exitosa."):
                return render_to_response('InventarioFrontEnd/inventario.html',{'lista_items': search_items(None,None,False),'mensaje':mensaje})
            else:
                return render_to_response(request, 'InventarioFrontEnd/item.html', {'form': form,'mensaje':mensaje})
    else:
        if request.method != 'POST':
            form = InventarioForm()
    return render(request, 'InventarioFrontEnd/item.html', {'form': form,'editing': False})

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
            try:
                flag = request.POST['circulando']
            except:
                flag = False
            mensaje = edit_item(request.POST['codigo'], request.POST['nombre'], request.POST['descripcion'], request.POST['cantidad'], request.POST['costo_unitario'], flag, request.POST['categoria'], request.POST['proveedor'])
            return render_to_response('InventarioFrontEnd/inventario.html',{'lista_items': search_items(None,None,False),'mensaje':mensaje})
    return render(request, 'InventarioFrontEnd/item.html', {'form': form,'editing': True})

def eliminar_item(request):
    return HttpResponse(delete_item(request.GET['q']), content_type='text/plain')

class InventarioForm(forms.ModelForm):   
    codigo = forms.CharField(required=True,max_length=30)
    nombre = forms.CharField(required=True,max_length=50)
    descripcion = forms.CharField(required=True,max_length=500)
    categoria = forms.ModelChoiceField(queryset=get_categories())
    proveedor = forms.ModelChoiceField(queryset=get_providers())
    costo_unitario = forms.FloatField(required=True)
    cantidad = forms.IntegerField(required=True)
    activo = forms.BooleanField(required=False,initial=True)
    class Meta:
        model = Item
        
        
