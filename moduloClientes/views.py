# Create your views here.
from moduloClientes.models import Cliente, Consultas
from django.shortcuts import render_to_response, render
from django.core.exceptions import ValidationError
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Q
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.http.response import Http404
from django.contrib.auth.decorators import login_required
from datetime import datetime, date
from django.contrib.admin.templatetags.admin_list import register


def clientes(request):
    """
    Muestra los clientes que se encuentran ingresados en el sistema

    **Context**

    ``RequestContext``

    ``Cliente``
        Objetos de :model:`moduloClientes.Cliente`.

    **Template:**

    :template:`ClientesFrontEnd/clientes.html`

    """
    list_clientes = Cliente.objects.all()
    usuario = request.user
    return render_to_response('ClientesFrontEnd/clientes.html',{'l_clienetes': list_clientes, 'user': usuario})

def consultas(request):
    """
    Muestra las consultas de cada cliente

    **Context**

    ``RequestContext``

    ``Cliente``
        Objetos de :model:`moduloClientes.Consulta`.

    **Template:**

    :template:`ClientesFrontEnd/consultas.html`

    """
    list_consultas = Consultas.objects.all()
    usuario = request.user
    return render_to_response('ClientesFrontEnd/consultas.html',{'l_consultas': list_consultas, 'user': usuario})

def buscar_historia_clinica(request):
    clients = Cliente.objects.all()
    return render(request, 'ClientesFrontEnd/buscarHistoriaClinica.html',{'l_clientes':clients})

def historia_clinica(request):
    
    if 'q' in request.GET and request.GET['q']:
        #q = decode_id(request.GET['q'])
        q = request.GET['q']
        cliente_c = Cliente.objects.filter(id=int(q))[0]
        l_consultas = Consultas.objects.filter(cliente=cliente_c)
        
        if l_consultas :
            return render(request,'ClientesFrontEnd/historiaClinica.html',{'l_consultas': l_consultas})
        else:
            return render(request, 'ClientesFrontEnd/buscarHistoriaClinica.html', {'l_clientes':clientes,'error': True})
    else:
        raise Http404
        
def nuevo_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            try:
                c = Cliente(cedula=request.POST['cedula'],nombre=request.POST['nombre'],apellido1=request.POST['apellido1'],apellido2=request.POST['apellido2'],fecha_nacimiento=date(year=int(request.POST['fecha_nacimiento_year']),month=int(request.POST['fecha_nacimiento_month']),day=int(request.POST['fecha_nacimiento_day'])),telefonos=request.POST['telefonos'],direccion=request.POST['direccion'],e_mail1=request.POST['e_mail1'],e_mail2=request.POST['e_mail2'],ruc=request.POST['ruc'])
            except MultiValueDictKeyError:
                c = Cliente(cedula=request.POST['cedula'],nombre=request.POST['nombre'],apellido1=request.POST['apellido1'],apellido2=request.POST['apellido2'],telefonos=request.POST['telefonos'],direccion=request.POST['direccion'],e_mail1=request.POST['e_mail1'],e_mail2=request.POST['e_mail2'],ruc=request.POST['ruc'])
            c.save()
            return clientes(request)
    else:
        if request.method != 'POST':
            form = ClienteForm()
    return render(request, 'ClientesFrontEnd/nuevoCliente.html', {'form': form})

def nueva_consulta(request):
    """
    Ingresa una nueva consulta

    **Context**

    ``RequestContext``

    ``Consultas``
        Instancia de :model:`moduloContabilidad.Consultas`.
        
    **Template:**

    :template:`ClientesFrontEnd/nuevaConsulta.html`

    """
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            c=Cliente.objects.filter(pk=request.POST['cliente'])[0]
            try:
                con = Consultas(cliente=c,esfera=request.POST['esfera'],cilindro=request.POST['cilindro'],eje=request.POST['eje'],av=request.POST['av'],add=request.POST['add'],dp=request.POST['dp'],fecha=date(year=int(request.POST['fecha_year']),month=int(request.POST['fecha_month']),day=int(request.POST['fecha_day'])),Diagnostico=request.POST['Diagnostico'],Observaciones=request.POST['Observaciones'],vista=request.POST['vista'],ojo=request.POST['ojo'],estado=request.POST['estado'])
            except MultiValueDictKeyError:
                con = Consultas(cliente=c,esfera=request.POST['esfera'],cilindro=request.POST['cilindro'],eje=request.POST['eje'],av=request.POST['av'],add=request.POST['add'],dp=request.POST['dp'],Diagnostico=request.POST['Diagnostico'],Observaciones=request.POST['Observaciones'],vista=request.POST['vista'],ojo=request.POST['ojo'],estado=request.POST['estado'])
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
                c.fecha_nacimiento = date(year=int(request.POST['fecha_nacimiento_year']),month=int(request.POST['fecha_nacimiento_month']),day=int(request.POST['fecha_nacimiento_day']))
                c.telefonos = request.POST['telefonos']
                c.direccion = request.POST['direccion']
                c.e_mail1 = request.POST['e_mail1']
                c.e_mail2 = request.POST['e_mail2']
                c.ruc = request.POST['ruc']
                c.save()
                return clientes(request)
    return render(request, 'ClientesFrontEnd/nuevoCliente.html', {'form': form})

def marcar_consulta(request):
    try:     
        cons = Consultas.objects.get(pk=int(request.GET['q']))
    except Exception:
        raise Http404
    
    if request.method == 'GET':
        if cons:
            #Esto marca al estado como 'REALIZADA'
            cons.estado = Consultas.ESTADO_CHOICES[1][0]
            cons.save()
        else:
            raise Http404
    return consultas(request)

def editar_consulta(request):
    """
    Edita una consulta

    **Context**

    ``RequestContext``

    ``Consultas``
        Instancia de :model:`moduloContabilidad.Consultas`.
        
    **Template:**

    :template:`ClientesFrontEnd/nuevaConsulta.html`

    """
    try:     
        cons = Consultas.objects.get(pk=int(request.GET['q']))
    except Exception:
        raise Http404
    
    if request.method != 'POST':
        if cons:
            form = ConsultaForm(instance=cons)
            form.id = int(request.GET['q'])
            if form.is_valid():
                form.save()
        else:
            raise Http404
    else:
        if request.method == 'POST':
            form = ConsultaForm(request.POST)
            if form.is_valid():
                cons.estado = request.POST['estado']
           
                cons.save()
                return consultas(request)
    return render(request, 'ClientesFrontEnd/nuevaConsulta.html', {'form': form})

@login_required
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

@login_required
def eliminar_consulta(request): 
    """
    Elimina una consulta

    **Context**

    ``RequestContext``

    ``Consultas``
        Instancia de :model:`moduloContabilidad.Consultas`.
        
    """ 
    try:       
        c = Consultas.objects.get(pk=int(request.GET['q']))
    except Exception:
        raise Http404
    if c:
        c.delete()
    else:
        raise Http404
    return consultas(request)

def create_nuevo_cliente(cedula,nombre,apellido1,apellido2,fecha_nacimiento,telefonos,direccion,e_mail1,e_mail2,ruc):
    cliente = Cliente(cedula=cedula,nombre=nombre,apellido1=apellido1,apellido2=apellido2,fecha_nacimiento=fecha_nacimiento,telefonos=telefonos,direccion=direccion,e_mail1=e_mail1,e_mail2=e_mail2,ruc=ruc)
    cliente.save()

def create_nueva_consulta(cliente,esfera,cilindro,eje,av,add,dp,fecha,Diagnostico,Observaciones,vista,ojo,estado):
    """
    Crear una nueva consulta

    **Context**

    ``RequestContext``

    ``Consultas``
        Instancia de :model:`moduloContabilidad.Consultas`.
        
    """ 
    consulta = Consultas(cliente,esfera,cilindro,eje,av,add,dp,fecha,Diagnostico,Observaciones,vista,ojo,estado)
    consulta.save()

class ClienteForm(forms.ModelForm):
  
    id = forms.IntegerField(required=False)
    cedula = forms.RegexField(max_length=10,required=False, regex=r'^[0-9]+')
    nombre = forms.CharField(max_length=30)
    apellido1 = forms.CharField(max_length=30,required=False)
    apellido2 = forms.CharField(max_length=30,required=False)
    fecha_nacimiento = forms.DateField(widget=SelectDateWidget(years=range(datetime.today().year-99, datetime.today().year+1 )),required=False)
    #maximo cuatro telefonos separados por coma
    telefonos = forms.RegexField(max_length=10, regex=r'^[0-9]+')
    direccion = forms.CharField(max_length=100)
    e_mail1 = forms.EmailField(required=False)
    e_mail2 = forms.EmailField(required=False)
    ruc = forms.RegexField(max_length=15, regex=r'^[0-9]+')
    
    class Meta:
        model = Cliente
        

def validate_cilindro(value):
    """
    Valida que el cilindro no pueda ser un número negativo
        
    """ 
    if value > 0:
        raise ValidationError('%s debe ser un numero negativo'% value)
    
def validate_eje(value):
    """
    Valida que el eje no pueda ser mayor a 180 ni negativo
        
    """ 
    if value >180:
        raise ValidationError('%s es un numero mayor a 180 grados'% value)
    if value <0:
        raise ValidationError('%s no puede ser un numero negativo'% value)    

def validate_add(value):
    """
    Valida que el add no pueda ser negativo
        
    """ 
    if value <0:
        raise ValidationError('%s no puede ser un numero negativo'% value)

def validate_dp(value):
    """
    Valida que el dp no pueda ser negativo
        
    """ 
    if value <0:
        raise ValidationError('%s no puede ser un numero negativo'% value)

class ConsultaForm(forms.ModelForm):
    """
    Crea un nuevo formulario de Cliente
        
    """ 
    id = forms.IntegerField(required=False)
    VISTA_CHOICES = (
                     ('LEJOS', 'LEJOS'),
                     ('CERCA', 'CERCA'),
                     )
    OJO_CHOICES = (
                   ('DERECHO', 'DERECHO'),
                   ('IZQUIERDO', 'IZQUIERDO'),
                   )
    
    ESTADO_CHOICES = (
                   ('PENDIENTE', 'PENDIENTE'),
                   ('REALIZADA', 'REALIZADA'),
                   )
    AV_CHOICES = (
                   ('2.0', '20/10'),
                   ('6.66', '20/13'),
                   ('1.33', '20/15'),
                   ('1.0', '20/20'),
                   ('0.8', '20/25'),
                   ('0.66', '20/30'),  
                   ('0.5', '20/40'),
                   ('0.4', '20/50'), 
                   ('0.28', '20/70'),  
                   ('0.2', '20/100'),
                   ('0.1', '20/200'),
                   )
    
    cliente=forms.ModelChoiceField(queryset=Cliente.objects.all())
    vista = forms.ChoiceField(choices=VISTA_CHOICES)
    ojo = forms.ChoiceField(choices=OJO_CHOICES)      
    estado = forms.ChoiceField(choices=ESTADO_CHOICES)
    esfera=forms.DecimalField(max_digits=5,decimal_places=3)
    cilindro=forms.DecimalField(max_digits=5,decimal_places=3,validators=[validate_cilindro])
    eje=forms.IntegerField(validators=[validate_eje])
    av=forms.ChoiceField(choices=AV_CHOICES)
    
    add=forms.DecimalField(max_digits=5,decimal_places=3)
    
        
    dp=forms.DecimalField(max_digits=5,decimal_places=3)
    
    fecha=forms.DateField(widget=SelectDateWidget(),required=False)
    Diagnostico = forms.CharField(widget=forms.Textarea(attrs={'cols':'100','rows':'4'}),required=False)
    Observaciones = forms.CharField(widget=forms.Textarea(attrs={'cols':'100','rows':'4'}),required=False)
   
   

    class Meta:
        model = Consultas 