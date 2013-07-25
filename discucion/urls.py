from django.conf.urls import patterns, include, url
from django.conf import settings


urlpatterns = patterns('',
 url(r'^comentario/(?P<p_id>\d+)/$', 'discucion.views.comentar', name='comentar'),
 url(r'^(?P<slug>[-\w]+)/$', 'discucion.views.discucion_gral', name='discucion_gral'),
 
 url(r'^(?P<slug>[-\w]+)/(?P<slug_grupo>[-\w]+)/acuerdos/$', 'discucion.views.acuerdos', name='acuerdos'),
 url(r'^(?P<slug>[-\w]+)/(?P<slug_grupo>[-\w]+)/$', 'discucion.views.discucion', name='discucion'),

 
)
