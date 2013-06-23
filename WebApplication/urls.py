from django.conf.urls.defaults import *
from django.contrib import admin
from WebApplication.views import *
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
    # Examples:
    # url(r'^$', 'WebApplication.views.home', name='home'),
    #url(r'^WebApplication/', include('moduloClientes.models')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    (r'^admin/', include(admin.site.urls)),
)
