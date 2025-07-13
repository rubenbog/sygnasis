from django.contrib import admin
from .models import Paciente, Diagnostico, Sintoma, Comorbilidad, Informe, Medicacion, Estudio, Resultado, Normativa

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'dni', 'edad', 'sexo', 'padre', 'madre', 'conyuge']
    search_fields = ['nombre', 'apellido', 'dni']
    list_filter = ['sexo']

@admin.register(Normativa)
class NormativaAdmin(admin.ModelAdmin):
    list_display = ('estudio', 'sexo', 'edad_min', 'edad_max', 'anios_estudio_min', 'anios_estudio_max', 'media', 'desviacion')
    list_filter = ('sexo', 'estudio')
    
admin.site.register(Diagnostico)
admin.site.register(Sintoma)
admin.site.register(Comorbilidad)
admin.site.register(Informe)
admin.site.register(Medicacion)
admin.site.register(Estudio)
admin.site.register(Resultado)

