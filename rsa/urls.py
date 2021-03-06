from django.conf.urls import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic.simple import direct_to_template

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rsa.views.home', name='home'),
     

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$','django.views.static.serve', 
                                  {'document_root': settings.MEDIA_ROOT}),
    url(r'^', include('proyectos.urls')),
    url(r'^usuarios/', include('usuarios.urls')),
    url(r'^intercambio/', include('discucion.urls')),
    ('^editar_datos/$', direct_to_template, {'template': 'editar_empresa.html'}),
   
)
