from django.db.models import (Model, CharField, TextField, ForeignKey,SlugField,
                              ManyToManyField, URLField, EmailField,
                              BooleanField, OneToOneField, FloatField,IntegerField,
                              DateTimeField,DateField,DecimalField,ImageField,FileField,PositiveIntegerField)

from django.utils.translation import ugettext as _
from django.db.models.signals import post_save,pre_delete
#dependencias
from django.contrib.auth.models import User

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from comunes.utils import get_upload_path
from django.template import defaultfilters
from proyectos.models import Proyecto

class Grupo_Discucion(Model):
    slug = SlugField( max_length=254)
    nombre = CharField(_('nombre'), max_length=254, null=False, blank=False)
    descripcion = TextField(_('descripcion'),null=True, blank=True)
    avatar = ImageField(_('avatar'), blank=True, upload_to=get_upload_path)    
    
    #releated objects
    proyecto=ForeignKey(Proyecto, verbose_name=_('Proyecto'), related_name = 'grupos')
    
    def __unicode__(self):
        return u'%s' % (self.nombre)
    
    #Meta
    class Meta:
        app_label = 'discucion' 
        db_table = 'grupos_discucion'
        verbose_name = 'grupo_discucion'
        verbose_name_plural = 'grupos_discuciones'
    def save(self, *args, **kwargs):
        self.slug =  defaultfilters.slugify(self.nombre)
        super(Grupo_Discucion, self).save(*args, **kwargs)
            

class Publicacion(Model):
    
    contenido = TextField('contenido', null=True, blank=True)
    fecha = DateTimeField(auto_now=True)
    
    #releated objects
    publisher = ForeignKey(User, verbose_name=_('autor'), related_name = 'publicaciones')
    grupo_discucion = ForeignKey(Grupo_Discucion, verbose_name=_('grupo_discucion'), related_name='grupo_publicaciones',null=True, blank=True)
    es_empresa = BooleanField( default=False)
    
    def __unicode__(self):
        return u'%s' % (self.contenido)    
    #Meta
    class Meta:
        app_label = 'discucion' 
        db_table = 'publicaciones'
        verbose_name = 'publicacion'
        verbose_name_plural = 'publicaciones'


class Comentario(Model):
    
    contenido = TextField(_('contenido'))
    date = DateTimeField(auto_now=True)
    
    #releated objects
    autor = ForeignKey(User, verbose_name=_('autor'), related_name = 'comentarios')
    publicacion = ForeignKey(Publicacion, verbose_name=_('autor'), related_name = 'comentarios')
    es_empresa = BooleanField( default=False)
        
    def __unicode__(self):
        return u'%s' % (self.contenido ) 

    #Meta
    class Meta:
        app_label = 'discucion' 
        db_table = 'comentarios'
        verbose_name = 'comentario'
        verbose_name_plural = 'comentarios'

ESTADOS_CHOICES= (
        ('1', 'Actual'),
        ('2','Potencial'),
        ('3','Mitigado'),
    )
CRITICO_CHOICES= (
        ('1', 'Alta'),
        ('2','Media'),
        ('3','Baja'),
    )
class Acuerdo(Model):
    titulo =CharField(_('nombre'), max_length=254, null=False, blank=False)
    descripcion = TextField(_('content'), max_length=420, null=True, blank=True)
    fecha = DateTimeField()
    estado_problema = CharField(max_length=2, choices=ESTADOS_CHOICES)
    nivel_criticidad = CharField(max_length=2, choices=CRITICO_CHOICES)
    
    
    #releated objects
    grupo_discucion = ForeignKey(Grupo_Discucion, verbose_name=_('grupo_discucio'), related_name = 'acuerdos',null=True, blank=True)
    
    
    def __unicode__(self):
        return u'%s' % (self.contenido)
    
    #Meta
    class Meta:
        app_label = 'discucion' 
        db_table = 'acuerdos'
        verbose_name = 'acuerdo'
        verbose_name_plural = 'acuerdos'
