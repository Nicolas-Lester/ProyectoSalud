from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'texto_corto', 'etiqueta')
    list_filter = ('etiqueta', 'fecha')
    search_fields = ('texto',)
    date_hierarchy = 'fecha'
    
    def texto_corto(self, obj):
        return obj.texto[:60] + '...' if len(obj.texto) > 60 else obj.texto
    texto_corto.short_description = 'Texto'

