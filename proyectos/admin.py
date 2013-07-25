from django.contrib import admin
from models import Empresa,Proyecto


class EmpresaAdmin(admin.ModelAdmin):
    pass


class ProyectoAdmin(admin.ModelAdmin):
    pass




admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Proyecto,ProyectoAdmin)
