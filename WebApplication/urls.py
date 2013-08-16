from django.contrib import admin
from WebApplication.views import index, error404
from moduloInventario.views import inventario, nuevo_item, editar_item,\
    eliminar_item
from django.conf.urls import patterns, url, include
from moduloClientes.views import clientes, buscar_form, buscar_cliente,\
    nuevo_cliente, editar_cliente, eliminar_cliente, consultas, nueva_consulta
from moduloFacturacion.views import abonos, nuevo_abono, nueva_orden_pedido,\
    editar_orden_pedido, ordenes_pedido
from moduloAutenticacion.views import login, logout
from moduloContabilidad.views import gastos,cuentas_por_pagar, ingresos_egresos, nuevo_gasto

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       #Modulo Clientes configuracion url_path para funionalidad clientes
                       url(r'^clientes/$', clientes),
                       url(r'^busquedaClientes/$', buscar_form),
                       (r'^search/$', buscar_cliente),
                       url(r'^nuevoCliente/$', nuevo_cliente),
                       url(r'^nuevo_cliente/$', nuevo_cliente),
                       url(r'^editarCliente/$', editar_cliente),
                       url(r'^eliminarCliente/$', eliminar_cliente),
                       #Modulo Clientes configuracion url_path para funionalidad consultas
                       url(r'^consultas/$', consultas),
                       url(r'^nuevaConsulta/$', nueva_consulta),
                       #Modulo Inventario configuracion url_path para funionalidad items
                       url(r'^inventario/$', inventario),
                       url(r'^nuevoItem/$', nuevo_item),
                       url(r'^editarItem/$', editar_item),
                       url(r'^eliminarItem/$', eliminar_item),                       
                       #Modulo Contabilidad configuracion url_path para funionalidad abonos
                       url(r'^abonos/$', abonos),
                       url(r'^nuevoAbono/$', nuevo_abono),
                       #Modulo contabilidad EDGAR
                       url(r'^gastos/$', gastos),
                       url(r'^cuentas_por_pagar/$', cuentas_por_pagar),
                       url(r'^estado_perdidas_ganancias/$', ingresos_egresos),
                       url(r'^nuevoGasto/$', nuevo_gasto),
                       #Modulo Facturacion configuracion url_path para funionalidad ordenes de pedido
                       url(r'^crearOrdenPedido/$', nueva_orden_pedido),
                       url(r'^editarOrdenPedido/$', editar_orden_pedido),
                       url(r'^ordenesDePedido/$', ordenes_pedido),
                       #Modulo Autenticacion configuracion url_path para funionalidad login
                       url(r'^login/$', login),
                       url(r'^index/$', index),
                       url(r'^logout/$', logout),
                       (r'^admin/', include(admin.site.urls)),
)

handler404 = error404
handler500 = error404