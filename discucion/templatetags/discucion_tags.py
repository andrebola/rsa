from django import template
from django.conf import settings

register = template.Library()

def grupo_interes(interesado,proyecto):
    ret=""
    for pros in interesado.relacioninteresados_set.all():
        if pros.proyecto==proyecto:
            ret=pros.grupo_interes.nombre
    return ret
register.simple_tag(grupo_interes)

