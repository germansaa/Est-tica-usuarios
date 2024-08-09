from django.contrib import admin
from .models import tarea
# Register your models here.
class tareaAdm(admin.ModelAdmin):
    readonly_fields = ('creado', )
admin.site.register(tarea, tareaAdm)