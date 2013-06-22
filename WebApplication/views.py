from django.shortcuts import render_to_response, render
from django.http import HttpResponse
import datetime
from moduloClientes.models import Cliente
from django import forms
from django.http.response import HttpResponseRedirect
from django.forms.extras.widgets import SelectDateWidget
from django.utils.datastructures import MultiValueDictKeyError

def hello(request):
    return HttpResponse("Ola k ase... Programando en django o q ase? :B")

def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('dateapp/current_datetime.html',{'current_date': now})

def clientes(request):
    list_clientes = Cliente.objects.all()
    
    return render_to_response('dateapp/clientes.html',{'l_clienetes': list_clientes})

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
        form = ClienteForm(request.POST)
    return render(request, 'dateapp/nuevoCliente.html', {'form': form})

class ClienteForm(forms.Form):
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