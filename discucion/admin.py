from django.contrib import admin
from models import Grupo_Discucion,Publicacion,Comentario


class Grupo_DiscucionAdmin(admin.ModelAdmin):
    pass

class PublicacionAdmin(admin.ModelAdmin):
    pass

class ComentarioAdmin(admin.ModelAdmin):
    pass

admin.site.register(Grupo_Discucion,Grupo_DiscucionAdmin)
admin.site.register(Publicacion, PublicacionAdmin)
admin.site.register(Comentario,ComentarioAdmin)
