
from django.db.models import Q
from moduloInventario.models import Item
#from django.newforms import form_for_model
from django.core.context_processors import request
from django.shortcuts import render_to_response

# Create your views here.
#InventarioForm = form_for_model(Inventario)

def inventario(request):
    lista_items = Item.objects.all()
    
    return render_to_response('InventarioFrontEnd/inventario.html',{'lista_items': lista_items})