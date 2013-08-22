from django.contrib import admin
from WebApplication.views import index, error404
from moduloInventario.views import inventario, nuevo_item, editar_item,\
    ordenes_compras, nueva_orden_compra, editar_orden_compra,\
    nuevo_detalle_compra, editar_detalle_compra, proveedores, nuevo_proveedor,\
    editar_proveedor, categorias, nueva_categoria, editar_categoria,\
    detalles_compra, eliminar_detalle_compra
from django.conf.urls import patterns, url, include
from moduloClientes.views import clientes, buscar_form, buscar_cliente,\
    nuevo_cliente, editar_cliente, eliminar_cliente, consultas, nueva_consulta,\
    marcar_consulta, historia_clinica, buscar_historia_clinica
from moduloFacturacion.views import abonos, nuevo_abono, nueva_orden_pedido,\
    editar_orden_pedido, ordenes_pedido, ventas
from moduloAutenticacion.views import login, logout
from moduloContabilidad.views import gastos,cuentas_por_pagar, ingresos_egresos, nuevo_gasto,\
    editar_gasto, eliminar_gasto

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
                       url(r'^marcarConsultaYaRealizada/$', marcar_consulta),
                       url(r'^buscarHistoriaClinica/$', buscar_historia_clinica),
                       url(r'^historiaClinica/$', historia_clinica),
                       #Modulo Inventario configuracion url_path para funionalidad items
                       url(r'^proveedores/$',proveedores),
                       url(r'^nuevoProveedor/$',nuevo_proveedor),
                       url(r'^editarProveedor/$',editar_proveedor),
                       url(r'^categorias/$',categorias),
                       url(r'^nuevaCategoria/$',nueva_categoria),
                       url(r'^editarCategoria/$',editar_categoria),
                       url(r'^inventario/$', inventario),
                       url(r'^nuevoItem/$', nuevo_item),
                       url(r'^editarItem/$', editar_item),
                       url(r'^ordenesCompra/$',ordenes_compras),
                       url(r'^nuevaOrdenCompra/$',nueva_orden_compra),
                       url(r'^editarOrdenCompra/$',editar_orden_compra),
                       url(r'^detallesCompra/$',detalles_compra),
                       url(r'^nuevoDetalleCompra/$',nuevo_detalle_compra),
                       url(r'^editarDetalleCompra/$',editar_detalle_compra),
                       url(r'^eliminarDetalleCompra/$',eliminar_detalle_compra),                    
                       #Modulo Contabilidad configuracion url_path para funionalidad abonos
                       url(r'^abonos/$', abonos),
                       url(r'^nuevoAbono/$', nuevo_abono),
                       #Modulo contabilidad EDGAR
                       url(r'^gastos/$', gastos),
                       url(r'^cuentas_por_pagar/$', cuentas_por_pagar),
                       url(r'^estado_perdidas_ganancias/$', ingresos_egresos),
                       url(r'^nuevoGasto/$', nuevo_gasto),
                       url(r'^editarGasto/$',editar_gasto),
                       url(r'^eliminarGasto/$',eliminar_gasto),
                       #Modulo Facturacion configuracion url_path para funionalidad ordenes de pedido
                       url(r'^crearOrdenPedido/$', nueva_orden_pedido),
                       url(r'^editarOrdenPedido/$', editar_orden_pedido),
                       url(r'^ordenesDePedido/$', ordenes_pedido),
                       url(r'^ventasDiarias/$', ventas),
                       #Modulo Autenticacion configuracion url_path para funionalidad login
                       url(r'^login/$', login),
                       url(r'^index/$', index),
                       url(r'^logout/$', logout),
                       #documentacion
                       (r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       (r'^admin/', include(admin.site.urls)),
)

handler404 = error404
handler500 = error404