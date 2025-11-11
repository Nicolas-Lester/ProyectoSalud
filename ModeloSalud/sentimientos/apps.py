"""
Configuración de la aplicación de sentimientos.
"""

from django.apps import AppConfig


class SentimientosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sentimientos'
