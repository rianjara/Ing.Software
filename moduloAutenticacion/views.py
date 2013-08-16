from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required

from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from WebApplication.views import index

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        if form.is_valid:
            user = request.POST['username']
            password = request.POST['password']
            access = authenticate(username=user, password=password)
            if access is not None:
                if access.is_active:
                    auth_login(request, access)
                    redirect = request.GET.get('next', '/index')
                    return HttpResponseRedirect(redirect)
                else:
                    return render_to_response('AutenticacionFrontEnd/login.html',{'form': form}, context_instance = RequestContext(request))
            else:
                return render_to_response('AutenticacionFrontEnd/login.html',{'form': form}, context_instance = RequestContext(request))
    else:
        form = AuthenticationForm()
        return render_to_response('AutenticacionFrontEnd/login.html',{'form': form}, context_instance = RequestContext(request))
    
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/index')