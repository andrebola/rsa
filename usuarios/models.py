from django.db.models import (Model, CharField, TextField, ForeignKey,
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
from comunes.models import Lugar
from proyectos.models import Empresa, Proyecto,GrupoInteres



GENERO= (
    ('M', _('Masculino')),   
    ('F', _('Femenino')),
)
EDADES= (
    ('1', 'menos de 18'),   
    ('2', '18 - 30'),
    ('3', '30 - 60'),
    ('4', 'mas de 60'),
)
TIPO_INTERES= (
    ('1', 'Neutro'),   
    ('2', 'Positivo'),
    ('3', 'Negativo'),
)
class Interesado(Model):

    
    avatar = ImageField(_('avatar'), blank=True, upload_to=get_upload_path)
    direccion = CharField('direccion', max_length=254,null=True, blank=True)
    genero= CharField('genero', max_length = 1, choices = GENERO,null=True, blank=True)
    ocupacion = CharField('ocupacion', max_length=254,null=True, blank=True)
    edad = CharField('edad', max_length=1,choices = EDADES,null=True, blank=True) 
        
    #releated objects
    user=OneToOneField(User,verbose_name='user',related_name = 'interesado')
    empresa = ForeignKey(Empresa, verbose_name='empresa', related_name = 'administradores',null=True, blank=True)
    lugar = ForeignKey(Lugar, verbose_name='lugar', related_name = 'interesados',null=True, blank=True)
    proyectos_interes = ManyToManyField(Proyecto, verbose_name='proyectos', related_name = 'interesados',null=True, blank=True,through='RelacionInteresados')
    
    def __unicode__(self):
        return u'%s %s' % (self.user.first_name, self.user.last_name) 

    #Meta
    class Meta:
        app_label = 'usuarios' 
        db_table = 'interesados'
        verbose_name = 'interesado'
        verbose_name_plural = 'interesados'
        
    
def crear_user_interesado(sender, instance, created, **kwargs):
    if created:
        Interesado.objects.create(user=instance)
        #User_language.objects.create(user=instance,language=None)

post_save.connect(crear_user_interesado, sender=User)

 
class RelacionInteresados(Model):
    interesado = ForeignKey(Interesado)
    proyecto = ForeignKey(Proyecto)
    grupo_interes = ForeignKey(GrupoInteres)
    tipo_interes = CharField('tipo Interes', max_length = 1, choices = TIPO_INTERES,null=True, blank=True)
