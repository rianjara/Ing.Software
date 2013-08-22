# Create your views here.

from moduloContabilidad.models import Gastos,Cuentas_x_pagar
from moduloInventario.models import Orden_Compra
from moduloFacturacion.models import OrdenPedido
from django.shortcuts import render_to_response, render
from django.utils.datastructures import MultiValueDictKeyError
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.http.response import Http404
from django.contrib.auth.decorators import login_required
from datetime import datetime, date


def gastos(request):
    list_gastos = Gastos.objects.all()
    usuario = request.user 
    return render_to_response('ContabilidadFrontEnd/gastos.html',{'l_gastos': list_gastos, 'user': usuario})

def ingresos_egresos(request):
    #Ingresos
    mes = datetime.now().month
    list_ingresos = OrdenPedido.objects.filter(fecha_compra__month=mes)
    
    #Egresos
    mes = datetime.now().month
    list_egresos = Orden_Compra.objects.filter(fecha__month=mes)
    
    return render_to_response('ContabilidadFrontEnd/estadoPerdidasyGanancias.html',{'l_ingresos': list_ingresos, 'l_egresos': list_egresos})

def nuevo_gasto(request):
    """
    Ingresa un nuevo Gasto

    **Context**

    ``RequestContext``

    ``Gastos``
        Instancia de :model:`moduloContabilidad.Gastos`.
        
    **Template:**

    :template:`ContabilidadFrontEnd/nuevoGasto.html`

    """
    if request.method == 'POST':
        form = GastoForm(request.POST)
        if form.is_valid():
            try:
                c = Gastos(concepto=request.POST['concepto'],valor_gasto=request.POST['valor_gasto'],fecha_gasto=date(year=int(request.POST['fecha_gasto_year']),month=int(request.POST['fecha_gasto_month']),day=int(request.POST['fecha_gasto_day'])),beneficiario=request.POST['beneficiario'],factura=request.POST['factura'])
            except MultiValueDictKeyError:
                c = Gastos(concepto=request.POST['concepto'],valor_gasto=request.POST['valor_gasto'],beneficiario=request.POST['beneficiario'],factura=request.POST['factura'])
            c.save()
            return gastos(request)
    else:
        if request.method != 'POST':
            form = GastoForm()
    return render(request, 'ContabilidadFrontEnd/nuevoGasto.html', {'form': form})


def editar_gasto(request):
    """
    Edita un Gasto

    **Context**

    ``RequestContext``

    ``Gastos``
        Instancia de :model:`moduloContabilidad.Gastos`.
        
    **Template:**

    :template:`ContabilidadFrontEnd/nuevoGasto.html`

    """
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
                c.valor_gasto = request.POST['valor_gasto']
                c.fecha_gasto = date(year=int(request.POST['fecha_gasto_year']),month=int(request.POST['fecha_gasto_month']),day=int(request.POST['fecha_gasto_day']))
                c.beneficiario = request.POST['beneficiario']
                c.factura = request.POST['factura']
                c.save()
                return gastos(request)
    return render(request, 'ContabilidadFrontEnd/nuevoGasto.html', {'form': form})

@login_required
def eliminar_gasto(request):
    """
    Elimina un Gasto

    **Context**

    ``RequestContext``

    ``Gastos``
        Instancia de :model:`moduloContabilidad.Gastos`.
        
    """
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
    """
    Consulta de las cuentas por pagar 

    **Context**

    ``RequestContext``

    ``Cuentas_x_pagar``
        Objetos de :model:`moduloContabilidad.Cuentas_x_pagar`.

    **Template:**

    :template:`ContabilidadFrontEnd/cuentasporpagar.html`

    """
    list_cuentas_x_pagar = Cuentas_x_pagar.objects.all()  
    return render_to_response('ContabilidadFrontEnd/cuentasporpagar.html',{'l_cuentasxpagar': list_cuentas_x_pagar}) 

def editar_cuenta_x_pagar(request):
    """
    Edita una cuenta por pagar 

    **Context**

    ``RequestContext``

    ``Cuentas_x_pagar``
        Instancia de :model:`moduloContabilidad.Cuentas_x_pagar`.

    **Template:**

    :template:`ComntabilidadFrontEnd/editarcuenta.html`

    """         
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
    """
    Formulario de cuenta por pagar 

    """
    fecha_vencimiento = forms.DateField(widget=SelectDateWidget(years=range(datetime.today().year-99, datetime.today().year+1 )),required=False)
     
    class Meta:
        model = Cuentas_x_pagar

class GastoForm(forms.ModelForm):
    """
    Formulario de cuenta por pagar 

    """
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
