from django.contrib import admin
from models import Interesado


class InteresadoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Interesado,InteresadoAdmin)
