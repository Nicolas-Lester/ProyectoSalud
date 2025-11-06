from django.db import models

# Create your models here.

class Comment(models.Model):
    fecha = models.DateField(null=True, blank=True)
    texto = models.TextField()
    etiqueta = models.CharField(max_length=10, choices=[("positivo", "positivo"), ("negativo", "negativo")])

    def __str__(self):
        return f"{self.fecha} – {self.texto[:60]}..."