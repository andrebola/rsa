from django.contrib import admin
from models import Lugar


class LugarAdmin(admin.ModelAdmin):
    pass


admin.site.register(Lugar, LugarAdmin)
#admin.site.register(piston.models.Consumer)