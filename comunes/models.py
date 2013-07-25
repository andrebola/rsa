from django.db.models import (Model, CharField,ForeignKey,IntegerField,ImageField)

class Lugar(Model):
    nombre=CharField(max_length=250 , blank=True)
    nivel =IntegerField (null=True)
    padre= ForeignKey("self", null=True , blank=True)
   
    def __unicode__(self):
        return self.nombre
    class Meta:
        # ordeno por created en forma descendente
        ordering = ['nombre']