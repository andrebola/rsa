from django.db.models import (Model, CharField, TextField, ForeignKey,
                              ManyToManyField, URLField, EmailField,
                              BooleanField, OneToOneField, FloatField,IntegerField,
                              DateTimeField,DateField,DecimalField,ImageField,FileField,PositiveIntegerField,
                              SlugField)

from django.utils.translation import ugettext as _
from django.db.models.signals import post_save,pre_delete
#dependencias
from django.contrib.auth.models import User

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from comunes.utils import get_upload_path
from comunes.models import Lugar
from django.template import defaultfilters
from django.core.exceptions import ObjectDoesNotExist


def crear_usuario_empresa(sender, instance, created, **kwargs):
    if created:
        Empresa.objects.create(administrador=instance)
       
        
class Empresa(Model):
    
    nombre = CharField(_('nombre'), max_length=254, null=False, blank=False)
    descripcion = TextField(_('descripcion'),null=True, blank=True)
    avatar = ImageField(_('avatar'), blank=True, upload_to=get_upload_path)
    
   
    def __unicode__(self):
        return u'%s' % (self.nombre)    
    #Meta
    class Meta:
        app_label = 'proyectos' 
        db_table = 'empresas'
        verbose_name = 'empresa'
        verbose_name_plural = 'empresas'
    
  
    @classmethod
    def create(cls, nombre):
        empresa = cls(nombre=nombre)
        return empresa

       
    
    def save(self, *args, **kwargs):
        #post_save.connect(crear_usuario_empresa, sender=User)
        super(Empresa, self).save(*args, **kwargs)

ETAPAS_CHOICES= (
        ('1', 'No iniciado'),
        ('2','Analisis'),
        ('3','Implementacion'),
        ('4','Seguimiento y Control'),
        ('5','Cerrado'),
    )
CAT_CHOICES=(
    ('1', 'Mineria'),
    ('2','Acuicola'),
    ('3','Forestal'),
    ('4','Energia'),
    ('5','Otro'),
)
class Proyecto(Model):
    slug = SlugField( max_length=254)
    nombre = CharField(_('nombre'), max_length=254, null=False, blank=False)
    descripcion = TextField(_('descripcion'),null=True, blank=True)
    avatar = ImageField(_('avatar'), blank=True, upload_to=get_upload_path)
    video = CharField('video',max_length=254,null=True, blank=True)    
    etapa=CharField(max_length=2, choices=ETAPAS_CHOICES)
    clasificacion=CharField(max_length=2, choices=CAT_CHOICES)
    
    #releated objects
    empresa = ForeignKey(Empresa, verbose_name=_('empresa'), related_name = 'proyectos')
    lugar = ForeignKey(Lugar, verbose_name=_('lugar'), related_name = 'lugar_interesados')
    def save(self, *args, **kwargs):
        slug=get_slug(defaultfilters.slugify(self.nombre))
        self.slug=slug
        super(Proyecto, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return u'%s' % (self.nombre)
    
    
    #Meta
    class Meta:
        app_label = 'proyectos' 
        db_table = 'proyectos'
        verbose_name = 'proyecto'
        verbose_name_plural = 'proyectos'
            
def get_slug(slug):
    try:
        Proyecto.objects.get(slug=slug)
        slug=get_slug(slug+'2')
    except ObjectDoesNotExist:
        slug = slug
    return slug

class GrupoInteres(Model):
    nombre =  CharField(_('nombre'), max_length=254, null=False, blank=False)
    proyecto = ForeignKey(Proyecto,related_name = 'grupo_interes')
    def __unicode__(self):
        return u'%s' % (self.nombre)
