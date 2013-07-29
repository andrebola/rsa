from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    
    url(r'^registro/$', 'usuarios.views.registro_interesado_1', name='registro_interesado_1'),
    url(r'^registro/paso2/(?P<user_id>\w+)/$', 'usuarios.views.paso2', name='paso2'),
    url(r'^participar/(?P<slug>[-\w]+)/$', 'usuarios.views.participar', name='participar'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)