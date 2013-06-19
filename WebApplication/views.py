from django.shortcuts import render_to_response, render
from django.http import HttpResponse
import datetime
from django.template.loader import get_template
from moduloClientes.models import Cliente

def hello(request):
    return HttpResponse("Ola k ase... Programando en django o q ase? :B")

def current_datetime(request):
    now = datetime.datetime.now()
    #Forma simple para usar plantillas desde sistema de archivo
    #Esto no cuenta para archivos perdidos
    #t = get_template('current_datetime.html')
    #html = "<html><body> La hora e s: %s jojojo!! </bosy></html>" %now
    #html = t.render(Context({'current_date': now}))
    #return HttpResponse(html)
    return render_to_response('dateapp/current_datetime.html',{'current_date': now})

def clientes(request):
    list_clientes = Cliente.objects.all()
    
    return render_to_response('dateapp/clientes.html',{'l_clienetes': list_clientes})