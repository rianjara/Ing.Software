from django.conf.urls.defaults import *
from django.contrib import admin
from WebApplication.views import current_datetime, hello, style_flat_ui,\
    style_bootstrap, clientes, fuente1, fuente2
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       #(r'^admin/',include('django.contrib.admin.urls')),
                       #(r'^admin/', include(admin.site.urls)),
                       url(r'^time/$', current_datetime),
                       url(r'^hello/$', hello),
                       url(r'^clientes/$', clientes),
    # Examples:
    # url(r'^$', 'WebApplication.views.home', name='home'),
    #url(r'^WebApplication/', include('moduloClientes.models')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    (r'^admin/', include(admin.site.urls)),
)
