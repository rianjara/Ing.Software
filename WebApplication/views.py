from django.shortcuts import render_to_response
from django.http import HttpResponse
import datetime

def hello(request):
    return HttpResponse("Ola k ase... Programando en django o q ase? :B")

def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('ClientesFrontEnd/current_datetime.html',{'current_date': now})