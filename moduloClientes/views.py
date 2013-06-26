# Create your views here.
from moduloClientes.models import Cliente
from django.shortcuts import render_to_response, render
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Q
from django import forms
from django.forms.extras.widgets import SelectDateWidget


def clientes(request):
    list_clientes = Cliente.objects.all()
    
    return render_to_response('ClientesFrontEnd/clientes.html',{'l_clienetes': list_clientes})

def nuevo_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            try:
                c = Cliente(cedula=request.POST['cedula'],nombre=request.POST['nombre'],apellido1=request.POST['apellido1'],apellido2=request.POST['apellido2'],fecha_nacimiento=request.POST['fecha_nacimiento'],telefonos=request.POST['telefonos'],direccion=request.POST['direccion'],e_mail1=request.POST['e_mail1'],e_mail2=request.POST['e_mail2'],ruc=request.POST['ruc'])
            except MultiValueDictKeyError:
                c = Cliente(cedula=request.POST['cedula'],nombre=request.POST['nombre'],apellido1=request.POST['apellido1'],apellido2=request.POST['apellido2'],telefonos=request.POST['telefonos'],direccion=request.POST['direccion'],e_mail1=request.POST['e_mail1'],e_mail2=request.POST['e_mail2'],ruc=request.POST['ruc'])
            c.save()
            return clientes(request)
    else:
        if request.method != 'POST':
            form = ClienteForm()
    return render(request, 'ClientesFrontEnd/nuevoCliente.html', {'form': form})

def buscar_form(request):
    return render(request, 'ClientesFrontEnd/buscar.html')

def buscar_cliente(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        clientes = Cliente.objects.filter(Q(nombre__icontains=q) | Q(apellido1__icontains=q) | Q(apellido2__icontains=q))
        return render(request, 'ClientesFrontEnd/clientes.html', {'l_clienetes': clientes})
    else:
        return render(request, 'ClientesFrontEnd/clientes.html', {'error': True})
    
def editar_cliente(request):        
    c = Cliente.objects.get(pk=int(request.GET['q']))
    
    if request.method != 'POST':
        form = ClienteForm(instance=c)
        form.id = int(request.GET['q'])
        if form.is_valid():
            form.save()
    else:
        if request.method == 'POST':
            form = ClienteForm(request.POST)
            if form.is_valid():
                c.cedula = request.POST['cedula']
                c.nombre = request.POST['nombre']
                c.apellido1 = request.POST['apellido1']
                c.apellido2 = request.POST['apellido2']
                c.telefonos = request.POST['telefonos']
                c.direccion = request.POST['direccion']
                c.e_mail1 = request.POST['e_mail1']
                c.e_mail2 = request.POST['e_mail2']
                c.ruc = request.POST['ruc']
                c.save()
                return clientes(request)
    return render(request, 'ClientesFrontEnd/nuevoCliente.html', {'form': form})

def eliminar_cliente(request):        
    c = Cliente.objects.get(pk=int(request.GET['q']))
    c.delete()
    return clientes(request)

class ClienteForm(forms.ModelForm):
    id = forms.IntegerField(required=False)
    cedula = forms.CharField(max_length=10,required=False)
    nombre = forms.CharField(max_length=30)
    apellido1 = forms.CharField(max_length=30,required=False)
    apellido2 = forms.CharField(max_length=30,required=False)
    fecha_nacimiento = forms.DateField(widget=SelectDateWidget(),required=False)
    #maximo cuatro telefonos separados por coma
    telefonos = forms.CharField(max_length=43)
    direccion = forms.CharField(max_length=100)
    e_mail1 = forms.EmailField(required=False)
    e_mail2 = forms.EmailField(required=False)
    ruc = forms.CharField(max_length=15)
    
    class Meta:
        model = Cliente
    
class BuscarForm(forms.Form):
    query = forms.CharField()