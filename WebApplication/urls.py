from django.conf.urls.defaults import *
from django.contrib import admin
from moduloClientes.views import *
from WebApplication.views import current_datetime, hello, index, error404
from moduloFacturacion.views import *
from moduloInventario.views import inventario, nuevo_item, editar_item,\
    eliminar_item
from moduloAutenticacion.views import *

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
                       url(r'^consultas/$', consultas),
                       #url(r'^index/$', index),
                       url(r'^nuevaConsulta/$', nueva_consulta),
                       url(r'^inventario/$', inventario),
                       url(r'^nuevoItem/$', nuevo_item),
                       url(r'^editarItem/$', editar_item),
                       url(r'^eliminarItem/$', eliminar_item),
                       url(r'^editar_crearOrdenPedido/$', nueva_orden_pedido),
                       url(r'^abonos/$', abonos),
                       url(r'^nuevoAbono/$', nuevo_abono),
                       url(r'^login/$', login),
                       url(r'^index/$', index),
                       url(r'^logout/$', logout),
                       #url(r'^nuevoAbono/$', nuevo_abono),
                       (r'^admin/', include(admin.site.urls)),
)

handler404 = error404
handler500 = error404