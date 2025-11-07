from django.db import models

# Modelo para guardar historico de demanda
class DemandaPacientes(models.Model):
    fecha = models.DateField()
    dia_semana = models.IntegerField()  # 0=Lunes, 6=Domingo
    mes = models.IntegerField()
    pacientes = models.IntegerField()
    es_feriado = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Demanda de Pacientes'
        verbose_name_plural = 'Demanda de Pacientes'
    
    def __str__(self):
        return f"{self.fecha} - {self.pacientes} pacientes"
