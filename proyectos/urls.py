from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'proyectos.views.landing', name='landing'),
    url(r'^nuevo-proyecto/$', 'proyectos.views.crear_proyecto', name='nuevo_proyecto'),
    url(r'^registro/$', 'proyectos.views.registro_empresa_1', name='registro_empresa_1'),
    url(r'^registro/paso2/(?P<empresa_id>\w+)/$', 'proyectos.views.paso2', name='paso2'),
    url(r'^perfil/(?P<proyecto_id>\w+)/$', 'proyectos.views.proyecto_perfil', name='perfil'),
    url(r'^perfil-pro/(?P<proyecto_id>\w+)/$', 'proyectos.views.proyecto_perfil', name='perfil'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r"^login/$", "proyectos.views.mylogin", name="login"),
    url(r"^login_redirect/(?P<redirect>\w+)$", "proyectos.views.mylogin", name="login"),
    url(r'^logout/$', 'proyectos.views.logout', name='logout'),
    url(r"^listado_proyectos/$", "proyectos.views.lista_proyectos", name="lista_proyectos_none"),
    url(r"^listado_proyectos/(?P<opcion>\w+)$", "proyectos.views.lista_proyectos", name="lista_proyectos"),
    url(r"^ajax_proyectos/$", "proyectos.views.ajax_proyectos", name="ajax_proyectos"),
    url(r"^ajax_mis_proyectos/$", "proyectos.views.ajax_mis_proyectos", name="ajax_mis_proyectos"),
    
    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
