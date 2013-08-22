from django.shortcuts import render_to_response, render
from moduloFacturacion.models import OrdenPedido, Abono,\
    Item_OrdenPedido_Cantidad
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from moduloInventario.models import Item
from django.core.exceptions import ValidationError
from django.utils.datastructures import MultiValueDictKeyError
from datetime import datetime, date
from django.forms.models import inlineformset_factory
from django.forms import models, widgets
from django.forms.widgets import TextInput
from moduloClientes.models import Cliente
from django.http.response import Http404
import decimal


def ventas(request):
    list_ventas = OrdenPedido.objects.exclude(codigo_factura__isnull=True)
    return render_to_response('FacturacionFrontEnd/ordenesPedido.html',{'l_ordenes': list_ventas})

def ordenes_pedido(request):
    list_ordenes = OrdenPedido.objects.all()
    return render_to_response('FacturacionFrontEnd/ordenesPedido.html',{'l_ordenes': list_ordenes})

def nueva_orden_pedido(request):
    fset=models.BaseInlineFormSet
    OrdenFormSet = inlineformset_factory(OrdenPedido,Item_OrdenPedido_Cantidad,ItemCantidadForm,fset,can_delete=False,extra=10,max_num=9)
    formset = OrdenFormSet()
    orden_form = OrdenPedidoForm()
    
    if request.method == 'POST':
        orden_form = OrdenPedidoForm(request.POST)
        if orden_form.is_valid(): 
            
            orden = OrdenPedido(
                                codigo=request.POST['codigo'],
                                codigo_factura = request.POST['codigo_factura'],
                                fecha_compra=date(year=int(request.POST['fecha_compra_year']),month=int(request.POST['fecha_compra_month']),day=int(request.POST['fecha_compra_day'])),
                                fecha_facturacion=date(year=int(request.POST['fecha_facturacion_year']),month=int(request.POST['fecha_facturacion_month']),day=int(request.POST['fecha_facturacion_day'])),
                                cliente=Cliente.objects.filter(pk=request.POST['cliente'])[0],
                                detalle=request.POST['detalle']
                                )
            orden.save()
            
            save_items_x_cantidad_in_orden(request)
            return ordenes_pedido(request)
    else:
        if request.method != 'POST':
            orden_form=OrdenPedidoForm()
            formset = OrdenFormSet()    
    return render(request, 'FacturacionFrontEnd/formOrdenDePedido.html', {'orden_form': orden_form, 'formset':formset})

def save_item_cantidad(codigo,item,cantidad,precio_unitario):
    #update_item
    item1 = Item.objects.filter(codigo=item)[0]
    item1.cantidad = int(item1.cantidad)- int(cantidad)
    item1.save()
    item_orden1=Item_OrdenPedido_Cantidad(orden_pedido=OrdenPedido.objects.filter(pk=codigo)[0],
                    item=item1,
                    cantidad=cantidad,
                    precio_venta_unitario=precio_unitario,
                    porcentaje_descuento=0.0)                    
    item_orden1.save(force_insert=True)
    
def save_items_x_cantidad_in_orden(request):
    Item_OrdenPedido_Cantidad.objects.filter(orden_pedido=request.POST['codigo']).delete()
    for i in range(10-1):
        prefix = 'item_ordenpedido_cantidad_set-%d'% i
        
        if request.POST['%s-item'% prefix]:
            save_item_cantidad(request.POST['codigo'],
              request.POST['%s-item'%prefix],
              request.POST['%s-cantidad'%prefix],
              request.POST['%s-precio_venta_unitario'%prefix])

def get_valor_total_orden_pedido(orden_id):
    item_orden1 = Item_OrdenPedido_Cantidad.objects.filter(orden_pedido=orden_id)
    sum = 0
    for i in item_orden1:
        sum = sum + i.cantidad*i.precio_venta_unitario
    return sum
        

def editar_orden_pedido(request):
    fset=models.BaseInlineFormSet
    OrdenFormSet = inlineformset_factory(OrdenPedido,Item_OrdenPedido_Cantidad,ItemCantidadForm,fset,can_delete=False,extra=10,max_num=9)
    formset = OrdenFormSet()
    
    try:     
        orden_p0 = OrdenPedido.objects.get(pk=request.GET['q'])
        items_0 = Item_OrdenPedido_Cantidad.objects.filter(orden_pedido=orden_p0)
    except Exception:
        raise Http404
    
    if request.method != 'POST':
        if orden_p0:
            orden_form = OrdenPedidoForm(instance=orden_p0)
            #formset = OrdenFormSet(initial=items_0)#'''queryset=items_0'''
            items_formset = []
            sum = 0
            for item_i in items_0:
                items_formset.append({'cantidad': item_i.cantidad , 'item': item_i.item.codigo, 'precio_venta_unitario':item_i.precio_venta_unitario,'subtotal':item_i.cantidad*item_i.precio_venta_unitario})
                sum = sum + item_i.cantidad*item_i.precio_venta_unitario
            
            formset = OrdenFormSet(initial=items_formset)
            orden_form.sub_total = sum
            orden_form.iva = sum*decimal.Decimal(0.12)
            orden_form.total = sum*decimal.Decimal(1.12)
        else:
            raise Http404
    elif request.method == 'POST':
        orden_form = OrdenPedidoForm(request.POST)
        #if orden_form.is_valid():
        OrdenPedido.objects.filter(pk=request.GET['q']).update(
                            codigo_factura = request.POST['codigo_factura'],
                            fecha_compra=date(year=int(request.POST['fecha_compra_year']),month=int(request.POST['fecha_compra_month']),day=int(request.POST['fecha_compra_day'])),
                            fecha_facturacion=date(year=int(request.POST['fecha_facturacion_year']),month=int(request.POST['fecha_facturacion_month']),day=int(request.POST['fecha_facturacion_day'])),
                            cliente=Cliente.objects.filter(pk=request.POST['cliente'])[0],
                            detalle=request.POST['detalle']
                            )
        #orden_p0.update(force_update=True)
        save_items_x_cantidad_in_orden(request)
        return ordenes_pedido(request)
    return render(request, 'FacturacionFrontEnd/formOrdenDePedido.html', {'orden_form': orden_form, 'formset':formset})

def abonos(request):
    list_abonos = Abono.objects.all()
    return render_to_response('FacturacionFrontEnd/abonos.html',{'l_abonos': list_abonos})

def validate_monto(monto):
    if monto < 0:
        raise ValidationError('El %s debe ser mayor a cero'% monto)

def nuevo_abono(request):
    if request.method == 'POST':
        form = AbonoForm(request.POST)
        if form.is_valid():
            try:
                op = OrdenPedido.objects.filter(pk=request.POST['orden_pedido'])[0]
                a = Abono(fecha=date(year=int(request.POST['fecha_year']),month=int(request.POST['fecha_month']),day=int(request.POST['fecha_day'])),orden_pedido=op,tipo_pago=request.POST['tipo_pago'],monto=request.POST['monto'])
            
                #a = Abono(fecha=request.POST['fecha'],orden_pedido=request.POST['orden_pedido'],tipo_pago=request.POST['tipo_pago'],monto=request.POST['monto'])
            except MultiValueDictKeyError:
                op = OrdenPedido.objects.filter(pk=request.POST['orden_pedido'])[0]
                a = Abono(fecha=date(year=int(request.POST['fecha_year']),month=int(request.POST['fecha_month']),day=int(request.POST['fecha_day'])),orden_pedido=op,tipo_pago=request.POST['tipo_pago'],monto=request.POST['monto'])
            a.save()
            return abonos(request)
    else:
        if request.method != 'POST':
            form = AbonoForm()
    return render(request, 'FacturacionFrontEnd/nuevoAbono.html', {'form': form})
       

class AbonoForm(forms.ModelForm):
    
    TIPO_PAGO_CHOICES = (('EFECTIVO', 'Efectivo'),
                 ('CHEQUE', (('PCF','Banco Pacifico'),
                          ('PCH','Banco de Pichincha'),
                          ('GYQ','Banco de Guayaquil'),
                          ('AMZ','Banco Amazonas'),
                          ('PRO','Banco Produbanco'),
                          ('CTR','Banco Central del Ecuado'),
                          ('SLD','Banco Solidario'),
                          ('PRM','Banco Promerica'),
                          ('INT','Banco Internacional'),
                          ('BNF','Banco Nacional de Fomento'),
                          ('BGR','Banco General Ruminahui'),
                          ('LOJ','Banco de Loja'),
                          ('AUS','Banco del Austro'),
                          ('BLV','Banco Bolivariano'),
                          ('MCH','Banco de Machala'),
                          ('BCN','Banco Coopnacional'),
                          ('UNB','Banco Unibanco'),
                          )),
                 ('TARJETA_CREDITO',(('VIS','Visa'),
                                         ('MTC','Master Card'),
                                         ('AME','American Express'),
                                         ('CUO','Cuota Facil'),
                                         )),
                  ('TARJETA_DEBITO',(('PCF','Banco Pacifico'),
                                          ('PCH','Banco de Pichincha'),
                                          ('GYQ','Banco de Guayaquil'),
                                          ('AMZ','Banco Amazonas'),
                                          ('PRO','Banco Produbanco'),
                                          ('CTR','Banco Central del Ecuado'),
                                          ('SLD','Banco Solidario'),
                                          ('PRM','Banco Promerica'),
                                          ('INT','Banco Internacional'),
                                          ('BNF','Banco Nacional de Fomento'),
                                          ('BGR','Banco General Ruminahui'),
                                          ('LOJ','Banco de Loja'),
                                          ('AUS','Banco del Austro'),
                                          ('BLV','Banco Bolivariano'),
                                          ('MCH','Banco de Machala'),
                                          ('BCN','Banco Coopnacional'),
                                          ('UNB','Banco Unibanco'),
                                          ))
                  ,)
    
    fecha = forms.DateField(widget=SelectDateWidget)
    orden_pedido = forms.ModelChoiceField(queryset=OrdenPedido.objects.all())
    tipo_pago = forms.CharField(max_length=30,widget=forms.Select(choices=TIPO_PAGO_CHOICES),required=True)
    monto =  forms.DecimalField(max_digits=8,decimal_places=4,validators=[validate_monto],required=True)
    
    class Meta:
        model = Abono
        fields = ('fecha','orden_pedido','tipo_pago','monto')

class ItemCantidadForm(forms.ModelForm):
    subtotal = forms.DecimalField()
    class Meta:
        model = Item_OrdenPedido_Cantidad
        fields = ('cantidad', 'item', 'precio_venta_unitario','subtotal')
        widgets = {
                   'cantidad': TextInput(attrs={'size':'5','maxlength':'3', 'onkeypress':'return event.charCode >= 48 && event.charCode <= 57','style':'width: 60px;'}),
                   'subtotal': TextInput(attrs={'readonly':'readonly'}),
                   'precio_venta_unitario': TextInput(attrs={'onkeypress':'return event.charCode >= 48 && event.charCode <= 57 || event.charCode == 46 && this.indexOf(\'.\') == -1;','size':'11','maxlength':'10'})
                   }
        
    class Media:
        js = ('js/jquery.autocomplete.min.js', 'js/autocomplete-init.js',)
        css = {
            'all': ('css/jquery.autocomplete.css',),
        }
        
    def __init__(self, *args, **kwargs):
        super(ItemCantidadForm, self).__init__(*args, **kwargs)
        self.fields['item'].widget = widgets.TextInput(attrs={'class': 'autocomplete-me'})

class OrdenPedidoForm(forms.ModelForm):
    codigo = forms.CharField(max_length=10)    
    detalle = forms.CharField( required = False,widget=forms.Textarea(attrs={'cols':'100','rows':'4'}) )
    fecha_compra=forms.DateField(widget=SelectDateWidget(years=range(datetime.today().year-4, datetime.today().year+1 ),attrs={'style':'width: 100px;'}))
    fecha_facturacion=forms.DateField(widget=SelectDateWidget(years=range(datetime.today().year-4, datetime.today().year+1 ),attrs={'style':'width: 100px;'}),required=False)
    sub_total=forms.DecimalField(max_digits=8, decimal_places=4)
    iva=forms.DecimalField(max_digits=8, decimal_places=4)
    total=forms.DecimalField(max_digits=8, decimal_places=4)
    #items = forms.MultipleChoiceField()
    
    class Meta:
        model = OrdenPedido
