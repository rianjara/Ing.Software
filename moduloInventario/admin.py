from django.contrib import admin
from moduloInventario.models import Item, Categoria, Proveedor, Item_Adq_Proveedor, Item_Costo_Venta, Item_Adq_Pendiente

admin.site.register(Item_Costo_Venta)
admin.site.register(Item_Adq_Proveedor)
admin.site.register(Item_Adq_Pendiente)
admin.site.register(Item)
admin.site.register(Categoria)
admin.site.register(Proveedor)