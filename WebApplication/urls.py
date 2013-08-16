from django.conf.urls import *
from django.contrib import admin
from moduloClientes.views import buscar_form, clientes, buscar_cliente,\
    nuevo_cliente, editar_cliente, eliminar_cliente
from moduloInventario.views import nuevo_item, inventario, editar_item, ordenes_compras, nueva_orden_compra, editar_orden_compra, nuevo_detalle_compra, editar_detalle_compra
from WebApplication.views import current_datetime, hello, index, error404

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       #(r'^admin/',include('django.contrib.admin.urls')),
                       #(r'^admin/', include(admin.site.urls)),
                       url(r'^time/$', current_datetime),
                       url(r'^hello/$', hello),
                       url(r'^clientes/$', clientes),
                       #url(r'^client/(\d+)/$', 'view.buscar_cliente'),
                       url(r'^busquedaClientes/$', buscar_form),
                       (r'^search/$', buscar_cliente),
                       url(r'^nuevoCliente/$', nuevo_cliente),
                       url(r'^nuevo_cliente/$', nuevo_cliente),
                       url(r'^editarCliente/$', editar_cliente),
                       url(r'^eliminarCliente/$', eliminar_cliente),
                       url(r'^index/$', index),
                       url(r'^inventario/$', inventario),
                       url(r'^nuevoItem/$', nuevo_item),
                       url(r'^editarItem/$', editar_item),
                       url(r'^ordenesCompra/$',ordenes_compras),
                       url(r'^nuevaOrdenCompra/$',nueva_orden_compra),
                       url(r'^editarOrdenCompra/$',editar_orden_compra),
                       url(r'^nuevoDetalleCompra/$',nuevo_detalle_compra),
                       url(r'^editarDetalleCompra/$',editar_detalle_compra),
                       (r'^admin/', include(admin.site.urls)),
                       url(r'^$', index),
)

handler404 = error404
handler500 = error404