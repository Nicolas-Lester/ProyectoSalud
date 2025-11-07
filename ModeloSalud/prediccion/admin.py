from django.contrib import admin
from .models import DemandaPacientes

@admin.register(DemandaPacientes)
class DemandaPacientesAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'dia_semana', 'pacientes', 'es_feriado']
    list_filter = ['es_feriado', 'dia_semana']
    search_fields = ['fecha']
