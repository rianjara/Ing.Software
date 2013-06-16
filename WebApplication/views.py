'''
Created on 15/06/2013

@author: Richard Jara
'''
from django.http import HttpResponse
import datetime

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>la hora de ahora es: %s</body></html>" %now
    return HttpResponse(html)
