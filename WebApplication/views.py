from django.shortcuts import render


def index(request):
    return render(request, 'index.html')

##
# Handle 404 Errors
# @param request WSGIRequest list with all HTTP Request
def error404(request):
    # 1. Load models for this view
    #from idgsupply.models import My404Method

    # 2. Generate Content for this view
    # 3. Return Template for this view + Data
    return render(request, '404.html',{'message': 'All: %s' % request.request.META}, content_type='text/html; charset=utf-8', status=404)