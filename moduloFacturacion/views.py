from django.shortcuts import render_to_response, render
from moduloFacturacion.models import OrdenPedido, Abono
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from datetime import datetime
from django.http.response import HttpResponse
from django.forms.widgets import Textarea
from moduloInventario.models import Item
from django.core.exceptions import ValidationError
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required
from django.template import RequestContext


def ventas(request):
    list_ventas = OrdenPedido.objects.exclude(codigo_factura__isnull=True)
    return render_to_response('FacturacionFrontEnd/ventas.html',{'l_ventas': list_ventas})

def ordenes_pedido(request):
    list_ordenes = OrdenPedido.objects.all()
    return render_to_response('FacturacionFrontEnd/ordenesCompra.html',{'l_ordenes': list_ordenes})

def nueva_orden_pedido(request):
    form = OrdenPedidoForm()
    return render(request, 'FacturacionFrontEnd/formOrdenDePedido.html', {'form': form})
    #return HttpResponse("Hello, world. You're at the poll index.")
        
class OrdenPedidoForm(forms.ModelForm):        
    detalle = forms.CharField( widget=forms.Textarea )        
    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all())
    
    class Meta:
        model = OrdenPedido

def abonos(request):
    list_abonos = Abono.objects.all()
    authenticated = request.user.is_authenticated()
    
    return render_to_response('FacturacionFrontEnd/abonos.html',{'l_abonos': list_abonos, 'authenticated': authenticated})

def validate_monto(monto):
    if monto < 0:
        raise ValidationError('El %s debe ser mayor a cero'% monto)
        

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



@login_required
def nuevo_abono(request):
    if request.method == 'POST':
        form = AbonoForm(request.POST)
        if form.is_valid():
            try:
                a = Abono(fecha=request.POST['fecha'],orden_pedido=request.POST['orden_pedido'],tipo_pago=request.POST['tipo_pago'],monto=request.POST['monto'])
            except MultiValueDictKeyError:
                a = Abono(fecha=request.POST['fecha'],orden_pedido=request.POST['orden_pedido'],tipo_pago=request.POST['tipo_pago'],monto=request.POST['monto'])
            a.save()
            return abonos(request)
    else:
        if request.method != 'POST':
            form = AbonoForm()
    return render(request, 'FacturacionFrontEnd/nuevoAbono.html', {'form': form})



