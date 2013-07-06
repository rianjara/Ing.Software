from django.contrib import admin
from moduloInventario.models import Item, Categoria, Proveedor

admin.site.register(Item)
admin.site.register(Categoria)
admin.site.register(Proveedor)