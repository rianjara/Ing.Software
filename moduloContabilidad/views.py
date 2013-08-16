# Create your views here.

from moduloContabilidad.models import Gastos,Cuentas_x_pagar
from moduloInventario.models import Orden_Compra
from moduloFacturacion.models import OrdenPedido
from django.shortcuts import render_to_response, render
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Q
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.http.response import Http404
from django.contrib.auth.decorators import login_required
from datetime import datetime


def gastos(request):
    list_gastos = Gastos.objects.all()    
    return render_to_response('ContabilidadFrontEnd/gastos.html',{'l_gastos': list_gastos})

def ingresos_egresos(request):
    #Ingresos
    mes = datetime.now().month
    list_ingresos = OrdenPedido.objects.filter(fecha_compra__month=mes)
    
    #Egresos
    mes = datetime.now().month
    list_egresos = Orden_Compra.objects.filter(fecha__month=mes)
    
    return render_to_response('ContabilidadFrontEnd/estadoPerdidasyGanancias.html',{'l_ingresos': list_ingresos, 'l_egresos': list_egresos})

def nuevo_gasto(request):
    if request.method == 'POST':
        form = GastoForm(request.POST)
        if form.is_valid():
            try:
                c = Gastos(concepto=request.POST['concepto'],valor_gasto=request.POST['valor_gasto'],fecha_gasto=request.POST['fecha_gasto'],beneficiario=request.POST['beneficiario'],factura=request.POST['factura'])
            except MultiValueDictKeyError:
                c = Gastos(concepto=request.POST['concepto'],valor_gasto=request.POST['valor_gasto'],beneficiario=request.POST['beneficiario'],factura=request.POST['factura'])
            c.save()
            return gastos(request)
    else:
        if request.method != 'POST':
            form = GastoForm()
    return render(request, 'ContabilidadFrontEnd/nuevoGasto.html', {'form': form})


def editar_gasto(request):
    try:     
        c = Gastos.objects.get(pk=int(request.GET['q']))
    except Exception:
        raise Http404
    
    if request.method != 'POST':
        if c:
            form = GastoForm(instance=c)
            form.id = int(request.GET['q'])
            if form.is_valid():
                form.save()
        else:
            raise Http404
    else:
        if request.method == 'POST':
            form = GastoForm(request.POST)
            if form.is_valid():
                c.concepto = request.POST['concepto']
                c.valor_gasto = request.POST['nombre']
                c.fecha_gasto = request.POST['fecha_gasto']
                c.beneficiario = request.POST['beneficiario']
                c.factura = request.POST['factura']
                c.save()
                return gastos(request)
    return render(request, 'ContabilidadFrontEnd/nuevoGasto.html', {'form': form})

@login_required
def eliminar_gasto(request):
    try:   
        c = Gastos.objects.get(pk=int(request.GET['q']))
    except Exception:
        raise Http404
            
    if c:
        c.delete()
    else:
        raise Http404
    return gastos(request)
    
def cuentas_por_pagar(request):
    list_cuentas_x_pagar = Cuentas_x_pagar.objects.all()  
    return render_to_response('ContabilidadFrontEnd/cuentasporpagar.html',{'l_cuentasxpagar': list_cuentas_x_pagar}) 

def editar_cuenta_x_pagar(request):        
    try:     
        c = Cuentas_x_pagar.objects.get(pk=int(request.GET['q']))
    except Exception:
        raise Http404
    
    if request.method != 'POST':
        if c:
            form = CuentaxPagarForm(instance=c)
            form.id = int(request.GET['q'])
            if form.is_valid():
                form.save()
        else:
            raise Http404
    else:
        if request.method == 'POST':
            form =CuentaxPagarForm(request.POST)
            if form.is_valid():
                c.fecha_vencimiento = request.POST['fecha_vencimiento']
             
                c.save()
                return cuentas_por_pagar(request)
    return render(request, 'ComntabilidadFrontEnd/editarcuenta.html', {'form': form})
    
class CuentaxPagarForm(forms.ModelForm):
    fecha_vencimiento = forms.DateField(widget=SelectDateWidget(years=range(datetime.today().year-99, datetime.today().year+1 )),required=False)
     
    class Meta:
        model = Cuentas_x_pagar

class GastoForm(forms.ModelForm):
    id = forms.IntegerField(required=False)
    concepto = forms.CharField(max_length=30)
    valor_gasto=forms.DecimalField(max_digits=5,decimal_places=3)
    fecha_gasto = forms.DateField(widget=SelectDateWidget(years=range(datetime.today().year-99, datetime.today().year+1 )),required=False)
    beneficiario = forms.CharField(required=False, max_length=20)
    factura=forms.IntegerField(required=False)
     
    class Meta:
        model = Gastos
    
class BuscarForm(forms.Form):
    query = forms.CharField()
