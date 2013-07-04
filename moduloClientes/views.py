# Create your views here.
from moduloClientes.models import Cliente, Consultas
from django.shortcuts import render_to_response, render
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Q
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.http.response import Http404


def clientes(request):
    list_clientes = Cliente.objects.all()    
    return render_to_response('ClientesFrontEnd/clientes.html',{'l_clienetes': list_clientes})

def consultas(request):
    list_consultas = Consultas.objects.all()
    return render_to_response('ClientesFrontEnd/consultas.html',{'l_consultas': list_consultas})

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

def nueva_consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            try:
                con = Consultas(esfera=request.POST['esfera'],cilindro=request.POST['cilindro'],eje=request.POST['eje'],av=request.POST['av'],add=request.POST['add'],dp=request.POST['dp'],fecha=request.POST['fecha'],Diagnostico=request.POST['Diagnostico'],Observaciones=request.POST['Observaciones'],vista=request.POST['vista'],ojo=request.POST['ojo'],estado=request.POST['estado'])
            except MultiValueDictKeyError:
                con = Consultas(esfera=request.POST['esfera'],cilindro=request.POST['cilindro'],eje=request.POST['eje'],av=request.POST['av'],add=request.POST['add'],dp=request.POST['dp'],Diagnostico=request.POST['Diagnostico'],Observaciones=request.POST['Observaciones'])
            con.save()
            return consultas(request)
    else:
        if request.method != 'POST':
            form = ConsultaForm()
    return render(request, 'ClientesFrontEnd/nuevaConsulta.html', {'form': form})

def buscar_form(request):
    return render(request, 'ClientesFrontEnd/buscar.html')

def buscar_cliente(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']        
        clientes = Cliente.objects.filter(Q(nombre__icontains=q) | Q(apellido1__icontains=q) | Q(apellido2__icontains=q))
        if clientes :
            return render(request, 'ClientesFrontEnd/clientes.html', {'l_clienetes': clientes})
        else:
            return render(request, 'ClientesFrontEnd/clientes.html', {'error': True})
        
    else:
        list_clientes = Cliente.objects.all()
        return render(request, 'ClientesFrontEnd/clientes.html', {'l_clienetes': list_clientes})
    
def editar_cliente(request):
    try:     
        c = Cliente.objects.get(pk=int(request.GET['q']))
    except Exception:
        raise Http404
    
    if request.method != 'POST':
        if c:
            form = ClienteForm(instance=c)
            form.id = int(request.GET['q'])
            if form.is_valid():
                form.save()
        else:
            raise Http404
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
    try:   
        c = Cliente.objects.get(pk=int(request.GET['q']))
    except Exception:
        raise Http404
            
    if c:
        c.delete()
    else:
        raise Http404
    return clientes(request)

def eliminar_consulta(request):  
    try:       
        c = Consultas.objects.get(pk=int(request.GET['q']))
    except Exception:
        raise Http404
    if c:
        c.delete()
    else:
        raise Http404
    return consultas(request)

class ClienteForm(forms.ModelForm):
    id = forms.IntegerField(required=False)
    cedula = forms.RegexField(max_length=10,required=False, regex=r'^[0-9]+')
    nombre = forms.CharField(max_length=30)
    apellido1 = forms.CharField(max_length=30,required=False)
    apellido2 = forms.CharField(max_length=30,required=False)
    fecha_nacimiento = forms.DateField(widget=SelectDateWidget(),required=False)
    #maximo cuatro telefonos separados por coma
    telefonos = forms.RegexField(max_length=10, regex=r'^[0-9]+')
    direccion = forms.CharField(max_length=100)
    e_mail1 = forms.EmailField(required=False)
    e_mail2 = forms.EmailField(required=False)
    ruc = forms.RegexField(max_length=15, regex=r'^[0-9]+')
    
    class Meta:
        model = Cliente
    
class ConsultaForm(forms.ModelForm):
    id = forms.IntegerField(required=False)
  
    VISTA_CHOICES = (
                     ('1', 'LEJOS'),
                     ('2', 'CERCA'),
                     )
    OJO_CHOICES = (
                   ('1', 'DERECHO'),
                   ('2', 'IZQUIERDO'),
                   )
    ESTADO_CHOICES = (
                   ('1', 'PENDIENTE'),
                   ('2', 'REALIZADA'),
                   )
    esfera=forms.DecimalField(max_digits=5,decimal_places=3)
    cilindro=forms.DecimalField(max_digits=5,decimal_places=3)
    eje=forms.CharField(max_length=30)
    av=forms.DecimalField(max_digits=5,decimal_places=3)
    add=forms.DecimalField(max_digits=5,decimal_places=3)
    dp=forms.DecimalField(max_digits=5,decimal_places=3)
    fecha=forms.DateField(widget=SelectDateWidget(),required=False)
    Diagnostico = forms.CharField(widget=forms.Textarea,required=False)
    Observaciones = forms.CharField(widget=forms.Textarea,required=False)
    vista = forms.ChoiceField(choices=VISTA_CHOICES)
    ojo = forms.ChoiceField(choices=OJO_CHOICES)      
    estado = forms.ChoiceField(choices=ESTADO_CHOICES)
    
    class Meta:
        model = Consultas

class BuscarForm(forms.Form):
    query = forms.CharField()