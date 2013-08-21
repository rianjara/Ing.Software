from django.contrib import admin
from moduloInventario.models import Item, Categoria, Proveedor, Orden_Compra, Detalle_Orden_Compra

admin.site.register(Item)
admin.site.register(Categoria)
admin.site.register(Proveedor)
admin.site.register(Orden_Compra)
admin.site.register(Detalle_Orden_Compra)