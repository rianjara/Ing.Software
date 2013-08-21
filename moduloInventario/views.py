
from django.db.models import Q
#from django.contrib.auth import authenticate
from django.template import RequestContext
from moduloInventario.models import Item, Proveedor, Categoria, Orden_Compra, Detalle_Orden_Compra
from django.shortcuts import render_to_response, render, redirect
from django import forms

# Create your views here.

def get_provider(pv_id):
    try:
        return Proveedor.objects.get(id=pv_id)
    except:
        return None

def get_provider_by_social_reason(string):
    return Proveedor.objects.get(razon_social=string)

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
    try:
        get_provider_by_social_reason(pv_razon_social)
        return "Operacion Fallida. Ya existe un proveedor con la misma razon social."
    except:
        provider = Proveedor(nombre=pv_nombre,razon_social=pv_razon_social,ruc=pv_ruc,telefono=pv_telefono)
        provider.save()
        return "Operacion Exitosa. El proveedor ha sido ingresado en la base de datos."
    
def update_provider(proveedor,pv_nombre,pv_razon_social,pv_ruc,pv_telefono):
    try:
        tmp = get_provider_by_social_reason(pv_razon_social)
        if tmp.id != proveedor.id:
            return "Operacion Fallida. No puede asignar una razon social que ya esta siendo usado por otro proveedor."
    except:
        tmp = None
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
    try:
        proveedor = get_provider(p_id)
        return update_provider(proveedor, pv_nombre, pv_razon_social, pv_ruc, pv_telefono)
    except:
        return "Opercion Fallida. El proveedor cuyos datos desea modificar, no esta regitrado en la base de datos."

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
    try:
        get_category_by_name(pv_nombre)
        return "Operacion Fallida. Ya existe una categoria con el mismo nombre."
    except:
        category = Categoria(nombre=pv_nombre,descripcion=pv_descripcion)
        category.save()
        return "Operacion Exitosa. La categoria ha sido ingresada en la base de datos."
    
def update_category(categoria,p_nombre,p_descripcion):
    try:
        tmp = get_category_by_name(p_nombre)
        if tmp.id != categoria.id:
            return "Operacion Fallida. No puede asignar un nombre que ya esta siendo usado por otra categoria."
    except:
        tmp = None
    categoria.nombre = p_nombre
    categoria.descripcion = p_descripcion
    categoria.save()
    return "Operacion Exitosa. Los datos de la categoria han sido actualizados."

def edit_category(p_id, pv_nombre,pv_descripcion):
    if pv_nombre is None:
        return "Operacion Fallida. El campo de el nombre esta vacio."
    try:
        category = get_category(p_id)
        return update_category(category, pv_nombre, pv_descripcion)
    except:
        return "Operacion Fallida. La categoria cuyos datos desea modificar, no esta registrada en la base de datos"

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
    try:
        item = get_item_by_code(pv_codigo)
        return "Operacion Fallida. Ya existe un item con el mismo codigo."
    except:
        item = Item(codigo=pv_codigo,nombre=pv_nombre,descripcion=pv_descripcion,cantidad=0,valor_venta=pf_valor_venta)
        item.categoria = get_category(pv_categoria)
        item.save()
        return "Operacion Exitosa. El item se ha creado con exito."
    
def update_item(item,p_codigo,p_nombre,p_descripcion,p_categoria,p_valor):
    try:
        tmp = get_item_by_code(p_codigo)
        if tmp.id != item.id:
            return "Operacion Fallida. No puede asignar un codigo que ya esta siendo usado por otro item."
    except:
        tmp = None
    item.codigo = p_codigo
    item.nombre = p_nombre
    item.descripcion = p_descripcion
    item.valor_venta = p_valor
    item.categoria = get_category(p_categoria)
    item.save()
    return "Operacion Exitosa. Los datos del item han sido actualizados."
   
def edit_item(p_id,pv_codigo,pv_nombre,pf_valor_venta,pv_descripcion,pv_categoria):
    if pv_codigo is None:
        return "Operacion Fallida. El campo de el codigo esta vacio."
    elif pv_nombre is None:
        return "Operacion Fallida. El campo de el nombre esta vacio."
    elif pf_valor_venta is None:
        return "Operacion Fallida. El campo de el valor de venta esta vacio."
    elif pv_categoria is None:
        return "Operacion Fallida. El campo de la categoria esta vacio."
    try:
        item = get_item(p_id)
        return update_item(item, pv_codigo, pv_nombre, pv_descripcion, pv_categoria, pf_valor_venta)
    except:
        return "Operacion Fallida. El item que desea modificar no existe en la base de datos."    

def new_order(p_id_proveedor,pi_factura,pd_fecha):
    if p_id_proveedor is None:
        return "Operacion Fallida. Debe seleccionar un proveedor."
    elif pi_factura is None:
        return "Operacion Fallida. Debe digitalizar el numero de la factura."
    elif pd_fecha is None:
        return "Operacion Fallida. Debe seleccionar la fecha de adquisicion."
    try:
        Orden_Compra.objects.get(proveedor=p_id_proveedor,factura=pi_factura)
        return "Operacion Fallida. Ya existe una orden para dicho proveedor con el mismo numero de factura"
    except:
        orden = Orden_Compra(factura=pi_factura,fecha=pd_fecha,valor_total=0)
        orden.proveedor = get_provider(p_id_proveedor)
        orden.save()
        return "Operacion Exitosa. Se ha ingresado la orden #%d"%orden.id
    
def update_order(orden,p_id_proveedor,pi_factura,pd_fecha):
    try:
        tmp = Orden_Compra.objects.get(proveedor=p_id_proveedor,factura=pi_factura)
        if tmp.id != orden.id:
            return "Operacion Fallida. No puede realizar la actualizacion debido que ya esxiste ese numero de factura para el proveedor seleccionado."
    except:
        tmp = None
    orden.factura = pi_factura
    orden.fecha = pd_fecha
    orden.proveedor = get_provider(p_id_proveedor)
    orden.save()
    return "Operacion Exitosa. Los datos de la orden han sido actualizados."
    
def edit_order(p_id,p_id_proveedor,pi_factura,pd_fecha):
    if p_id is None:
        return "Operacion Fallida. Falta el id del proveedor."
    elif p_id_proveedor is None:
        return "Operacion Fallida. Debe seleccionar un proveedor."
    elif pi_factura is None:
        return "Operacion Fallida. Debe digitalizar el numero de la factura."
    elif pd_fecha is None:
        return "Operacion Fallida. Debe seleccionar la fecha de adquisicion."
    try:
        orden = Orden_Compra.objects.get(id=p_id)
        return update_order(orden, p_id_proveedor, pi_factura, pd_fecha)
    except:
        return "Operacion Fallida. La orden que desea modificar no existe en la base de datos."
    
def new_order_detail(p_id_orden,p_id_item,pi_cantidad,pf_valor):
    if p_id_orden is None:
        return "Operacion Fallida. Falta el numero de la orden de compra."
    elif p_id_item is None:
        return "Operacion Fallida. No ha seleccionado el item."
    elif pi_cantidad is None:
        return "Operacion Fallida. Debe ingresar la cantidad de items."
    elif pf_valor is None:
        return "Operacion Fallida. Debe ingresar el valor unitario de cada item."
    try:
        Detalle_Orden_Compra.objects.get(orden=p_id_orden,item=p_id_item)
        return "Operacion Fallida. Ya se ha registrado el item en dicha orden de compra."
    except:
        detail = Detalle_Orden_Compra(cantidad=pi_cantidad,valor_unitario=pf_valor)
        detail.item = get_item(p_id_item)
        detail.orden = Orden_Compra.objects.get(id=p_id_orden)
        detail.orden.valor_total = unicode(float(detail.orden.valor_total) + (float(pf_valor))*(int(pi_cantidad)))
        detail.save()
        detail.orden.save()
        return "Operacion Exitosa. El item ha sido ingresado en la orden de compra."

def update_order_detail(detail,p_id_orden,p_id_item,pi_cantidad,pf_valor):
    try:
        tmp = Detalle_Orden_Compra.objects.get(item=p_id_item,orden=p_id_orden)
        if tmp.id != detail.id:
            return "Operacion Fallida. No puede realizar la actualizacion debido que ya esxiste ese item en dicha orden de compra."
    except:
        tmp = None
    total_en_item_old = (float(detail.valor_unitario))*(int(detail.cantidad))
    total_en_item_new = (float(pf_valor))*(int(pi_cantidad))
    detail.orden = Orden_Compra.objects.get(id=p_id_orden)
    detail.item = get_item(p_id_item)
    detail.cantidad = pi_cantidad
    detail.valor = pf_valor
    detail.orden.valor_total = unicode(float(detail.orden.valor_total) - total_en_item_old + total_en_item_new)
    detail.save()
    return "Operacion Exitosa. Los datos del detalle de la orden #%s han sido actualizados"%p_id_orden

def edit_order_detail(p_id_detail,p_id_orden,p_id_item,pi_cantidad,pf_valor):
    if p_id_orden is None:
        return "Operacion Fallida. Falta el numero de la orden de compra."
    elif p_id_item is None:
        return "Operacion Fallida. No ha seleccionado el item."
    elif pi_cantidad is None:
        return "Operacion Fallida. Debe ingresar la cantidad de items."
    elif pf_valor is None:
        return "Operacion Fallida. Debe ingresar el valor unitario de cada item."
    try:
        detail = Detalle_Orden_Compra.objects.get(id=p_id_detail)
    except:
        return "Operacion Fallida. El detalle de la orden que desea modificar no existe."
    return update_order_detail(detail,p_id_orden,p_id_item,pi_cantidad,pf_valor)
    
def delete_order_detail(p_id_detail):
    try:
        detail = Detalle_Orden_Compra.objects.get(id=p_id_detail)
        detail.delete()
        return "Operacion Exitosa. El detalle de compra ha sido eliminado"
    except:
        return "Operacion Fallida. El detalle que desea eliminar no se encuentra en la base de datos."

def proveedores(request):
    """
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)
    else:
    """
    return render_to_response('InventarioFrontEnd/proveedores.html',{'lista': Proveedor.objects.all()})

def nuevo_proveedor(request):
    """
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)
    else:
    """
    if 'action' in request.POST:
        if request.POST['action'] == 'none':
            form = ProveedorForm()
            return render_to_response('InventarioFrontEnd/proveedor.html', {'form': form,'editing': False},context_instance=RequestContext(request))
        elif request.POST['action'] == 'provider':
            form = ProveedorForm(request.POST)
            if form.is_valid():
                mensaje = new_provider(request.POST['nombre'], request.POST['razon_social'], request.POST['ruc'], request.POST['telefono'])
                if mensaje.startswith("Operacion Exitosa."):
                    return render_to_response('InventarioFrontEnd/proveedores.html',{'lista': Proveedor.objects.all(),'mensaje':mensaje})
                else:
                    return render_to_response('InventarioFrontEnd/proveedor.html', {'form': form,'mensaje':mensaje},context_instance=RequestContext(request))
            else:
                return render_to_response('InventarioFrontEnd/proveedor.html', {'form': form,'mensaje':form.errors},context_instance=RequestContext(request))
        else:
            return redirect('/index/')
    else:
        return redirect('/index/')

def editar_proveedor(request):
    """
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)
    else:
    """
    if not 'action' in request.POST: 
        return redirect('/index/')
    else: 
        if request.POST['action'] == 'none':
            form = ProveedorForm(instance=Item.objects.get(pk=request.POST['id']))
            form.id = request.POST['id']
            if form.is_valid():
                form.save()
                return render(request, 'InventarioFrontEnd/proveedor.html', {'form': form,'editing': True})
        elif request.POST['action'] == 'provider':
            form = ProveedorForm(request.POST)
            mensaje = edit_provider(request.POST['id'],request.POST['nombre'], request.POST['razon_social'], request.POST['ruc'], request.POST['telefono'])
            return render_to_response('InventarioFrontEnd/proveedores.html',{'lista': Proveedor.objects.all(),'mensaje':mensaje})
        else:
            return redirect('/index/')
        

def categorias(request):
    """
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)
    else:
    """
    return render_to_response('InventarioFrontEnd/categorias.html',{'lista': Categoria.objects.all()})

def nueva_categoria(request):
    """
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)
    else:
    """      
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            mensaje = new_category(request.POST['nombre'], request.POST['descripcion'])
            if mensaje.startswith("Operacion Exitosa."):
                return render_to_response('InventarioFrontEnd/categorias.html',{'lista': Categoria.objects.all(),'mensaje':mensaje})
            else:
                return render_to_response('InventarioFrontEnd/categoria.html', {'form': form,'mensaje':mensaje},context_instance=RequestContext(request))
        else:
            return render_to_response('InventarioFrontEnd/categoria.html', {'form': form,'mensaje':form.errors},context_instance=RequestContext(request))
    else:
        form = CategoriaForm()
        return render_to_response('InventarioFrontEnd/categoria.html', {'form': form,'editing': False},context_instance=RequestContext(request))

def editar_categoria(request):
    """
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)
    else:
    """      
    i = Item.objects.get(pk=(request.GET['q']))
    if request.method != 'POST':
        form = CategoriaForm(instance=i)
        form.id = request.GET['q']
        if form.is_valid():
            form.save()
    else:
        if request.method == 'POST':
            form = CategoriaForm(request.POST)
            mensaje = edit_category(request.POST['id'],request.POST['nombre'], request.POST['descripcion'])
            return render_to_response('InventarioFrontEnd/categorias.html',{'lista': Proveedor.objects.all(),'mensaje':mensaje})
    return render(request, 'InventarioFrontEnd/categoria.html', {'form': form,'editing': True})

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
    """
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)
    else:
    """      
    i = Item.objects.get(pk=(request.GET['q']))
    if request.method != 'POST':
        form = ItemForm(instance=i)
        form.id = request.GET['q']
        if form.is_valid():
            form.save()
    else:
        if request.method == 'POST':
            form = ItemForm(request.POST)
            mensaje = edit_item(request.POST['id'],request.POST['codigo'], request.POST['nombre'], request.POST['valor_venta'], request.POST['descripcion'], request.POST['categoria'])
            return render_to_response('InventarioFrontEnd/inventario.html',{'lista_items': search_items(None,None),'mensaje':mensaje})
    return render(request, 'InventarioFrontEnd/item.html', {'form': form,'editing': True})

def ordenes_compras(request):
    """
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)
    else:
    """
    return render_to_response('InventarioFrontEnd/ordenes_compra.html',{'lista': Orden_Compra.objects.all()})

def nueva_orden_compra(request):
    """
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)
    else:
    """      
    if request.method == 'POST':
        form = OrdenCompraForm(request.POST)
        if form.is_valid():
            mensaje = new_order(request.POST['proveedor'], request.POST['factura'], request.POST['fecha'])
            if mensaje.startswith("Operacion Exitosa."):
                return render_to_response('InventarioFrontEnd/ordenes_compra.html',{'lista': Orden_Compra.objects.all(),'mensaje':mensaje})
            else:
                return render_to_response('InventarioFrontEnd/compra.html', {'form': form,'mensaje':mensaje},context_instance=RequestContext(request))
        else:
            return render_to_response('InventarioFrontEnd/compra.html', {'form': form,'mensaje':form.errors},context_instance=RequestContext(request))
    else:
        form = OrdenCompraForm()
        return render_to_response('InventarioFrontEnd/compra.html', {'form': form,'editing': False},context_instance=RequestContext(request))

def editar_orden_compra(request):
    """
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)
    else:
    """      
    i = Orden_Compra.objects.get(pk=(request.GET['q']))
    if request.method != 'POST':
        form = OrdenCompraForm(instance=i)
        form.id = request.GET['q']
        if form.is_valid():
            form.save()
    else:
        if request.method == 'POST':
            form = OrdenCompraForm(request.POST)
            mensaje = edit_order(request.POST['id'],request.POST['proveedor'], request.POST['factura'], request.POST['fecha'])
            if mensaje.startswith("Operacion Exitosa."):
                return render_to_response('InventarioFrontEnd/ordenes_compra.html',{'lista': Orden_Compra.objects.all(),'mensaje':mensaje})
            else:
                return render(request, 'InventarioFrontEnd/compra.html', {'form': form,'editing': True,'mensaje': mensaje},context_instance=RequestContext(request))
    return render(request, 'InventarioFrontEnd/compra.html', {'form': form,'editing': True})

def detalles_compra(request):
    """
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)
    else:
    """
    if 'orden' in request.GET:
        return render_to_response('InventarioFrontEnd/detalles_compra.html',{'lista': Detalle_Orden_Compra.objects.filter(orden=request.GET['orden']),'orden':request.GET['orden']})
    else:
        return redirect('/index/')

def nuevo_detalle_compra(request):
    """
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)
    else:
    """
    if request.method == 'POST':
        form = DetalleOrdenCompraForm(request.POST)
        if form.is_valid():
            mensaje = new_order_detail(request.POST['orden'],request.POST['item'], request.POST['cantidad'], request.POST['valor_unitario'])
            if mensaje.startswith("Operacion Exitosa."):
                return render_to_response('InventarioFrontEnd/detalles_compra.html',{'lista': Detalle_Orden_Compra.objects.filter(orden=request.POST['orden']),'orden':request.POST['orden'],'mensaje':mensaje})
            else:
                return render_to_response('InventarioFrontEnd/compra_item.html', {'form': form,'mensaje':mensaje},context_instance=RequestContext(request))
        else:
            return render_to_response('InventarioFrontEnd/compra_item.html', {'form': form,'mensaje':form.errors},context_instance=RequestContext(request))
    else:
        form = DetalleOrdenCompraForm()
        form.initial={'orden': request.GET['orden']}
        return render_to_response('InventarioFrontEnd/compra_item.html', {'form': form,'editing': False},context_instance=RequestContext(request))

def editar_detalle_compra(request):
    """
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)
    else:
    """      
    i = Detalle_Orden_Compra.objects.get(pk=(request.GET['q']))
    if request.method != 'POST':
        form = DetalleOrdenCompraForm(instance=i)
        form.id = request.GET['q']
        print form.errors
        if form.is_valid():
            form.save()
    else:
        if request.method == 'POST':
            form = DetalleOrdenCompraForm(request.POST)
            mensaje = edit_order_detail(request.POST['id'],request.POST['orden'],request.POST['item'], request.POST['cantidad'], request.POST['valor_unitario'])
            if mensaje.startswith("Operacion Exitosa."):
                return render_to_response('InventarioFrontEnd/detalles_compra.html',{'lista': Detalle_Orden_Compra.objects.filter(orden=request.POST['orden'])})
            else:
                return render(request, 'InventarioFrontEnd/compra_item.html', {'form': form,'editing': True,'mensaje': mensaje,'orden_id':request.POST['orden']},context_instance=RequestContext(request))
    return render(request, 'InventarioFrontEnd/compra_item.html', {'form': form,'editing': True})

def eliminar_detalle_compra(request):
    """
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)
    else:
    """ 
    try:
        return delete_order_detail(request.GET['q'])
    except:
        "Operacion Fallida. El item que desea eliminar no se encuentra en dicha orden de compra."

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

class OrdenCompraForm(forms.ModelForm):
    proveedor = forms.ModelChoiceField(queryset=get_providers())
    factura = forms.IntegerField(required=True)
    fecha = forms.DateField(required=True)
    valor_total = forms.FloatField(required=False,initial=0)
    class Meta:
        model = Orden_Compra

class DetalleOrdenCompraForm(forms.ModelForm):
    item = forms.ModelChoiceField(queryset=search_items(None, None))
    orden = forms.ModelChoiceField(queryset=Orden_Compra.objects.all())
    cantidad = forms.IntegerField(required=True)
    valor_unitario = forms.FloatField(required=True,initial=0)
    class Meta:
        model = Detalle_Orden_Compra
        
