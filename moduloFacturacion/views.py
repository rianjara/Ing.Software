from django.shortcuts import render_to_response, render
from moduloFacturacion.models import OrdenPedido, Abono
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from datetime import datetime
from django.http.response import HttpResponse
from django.forms.widgets import Textarea
from moduloInventario.models import Item


def ventas(request):
    list_ventas = OrdenPedido.objects.exclude(codigo_factura__isnull=True)
    return render_to_response('FacturacionFrontEnd/ventas.html',{'l_ventas': list_ventas})

def ordenes_pedido(request):
    list_ordenes = OrdenPedido.objects.all()
    return render_to_response('FacturacionFrontEnd/ordenesCompra.html',{'l_ordenes': list_ordenes})

def abonos(request):
    list_abonos = Abono.objects.all()
    return render_to_response('FacturacionFrontEnd/abonos.html',{'l_abonos': list_abonos})

def nueva_orden_pedido(request):
    form = OrdenPedidoForm()
    return render(request, 'FacturacionFrontEnd/formOrdenDePedido.html', {'form': form})
    #return HttpResponse("Hello, world. You're at the poll index.")

class AbonoForm(forms.ModelForm):    
    class Meta:
        model = Abono
        fields = ('fecha','monto', 'tipo_pago', 'orden_pedido')
        widgets = {
            'fecha': SelectDateWidget(datetime.today().year+3,datetime.today().year+1),
        }
        
class OrdenPedidoForm(forms.ModelForm):        
    detalle = forms.CharField( widget=forms.Textarea )        
    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all())
    
    class Meta:
        model = OrdenPedido