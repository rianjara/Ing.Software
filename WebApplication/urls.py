from django.conf.urls.defaults import *
from django.contrib import admin
from moduloClientes.views import buscar_form, clientes, buscar_cliente,\
    nuevo_cliente, editar_cliente, eliminar_cliente, nueva_consulta
from WebApplication.views import current_datetime, hello, index, error404
from moduloFacturacion.views import nueva_orden_pedido
from moduloInventario.views import inventario, nuevo_item, editar_item,\
    eliminar_item

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

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
                       url(r'^nuevaConsulta/$', nueva_consulta),
                       url(r'^inventario/$', inventario),
                       url(r'^nuevoItem/$', nuevo_item),
                       url(r'^editarItem/$', editar_item),
                       url(r'^eliminarItem/$', eliminar_item),
                       url(r'^editar_crearOrdenPedido/$', nueva_orden_pedido),
                       (r'^admin/', include(admin.site.urls)),
)

handler404 = error404
handler500 = error404