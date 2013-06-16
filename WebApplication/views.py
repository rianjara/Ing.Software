from django.http import HttpResponse
import datetime
def hello(request):
    return HttpResponse("Hello world")

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body> La hora e s: %s jojojo!! </bosy></html>" %now
    return HttpResponse(html)