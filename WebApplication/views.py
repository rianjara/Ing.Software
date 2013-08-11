from django.shortcuts import render_to_response, render
from django.http import HttpResponse
import datetime
from django.template.context import Context
from django.template import loader

def hello(request):
    return HttpResponse("Ola k ase... Programando en django o q ase? :B")

def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('ClientesFrontEnd/current_datetime.html',{'current_date': now})

def index(request):
    return render(request, 'index.html', locals())

##
# Handle 404 Errors
# @param request WSGIRequest list with all HTTP Request
def error404(request):
    # 1. Load models for this view
    #from idgsupply.models import My404Method

    # 2. Generate Content for this view
    # 3. Return Template for this view + Data
    return render(request, '404.html',{'message': 'All: %s' % request.request.META}, content_type='text/html; charset=utf-8', status=404)