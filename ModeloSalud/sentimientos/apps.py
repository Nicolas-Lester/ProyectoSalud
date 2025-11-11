"""
Configuración de la aplicación de sentimientos.
Carga automáticamente los datos iniciales del CSV si la base de datos está vacía.
"""

from django.apps import AppConfig


class SentimientosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sentimientos'
    
    def ready(self):
        """
        Este método se ejecuta automáticamente cuando Django inicia.
        Aquí cargamos los comentarios del CSV si la tabla está vacía.
        """
        # Solo ejecutar en el proceso principal (no en reloader)
        import os
        if os.environ.get('RUN_MAIN') != 'true':
            return
        
        # Importar aquí para evitar errores de apps no cargadas
        from sentimientos.models import Comment
        from django.core.management import call_command
        
        try:
            # Verificar si la tabla está vacía
            if Comment.objects.count() == 0:
                print("\n" + "="*60)
                print("🔄 Primera ejecución detectada - Sentimientos")
                print("   Cargando comentarios iniciales desde CSV...")
                print("="*60 + "\n")
                
                # Llamar al comando load_comments automáticamente
                call_command('load_comments')
                
                print("\n" + "="*60)
                print("✅ Comentarios cargados correctamente")
                print("="*60 + "\n")
        
        except Exception as e:
            # Si hay error, mostrar pero no detener Django
            print(f"\n⚠️  No se pudieron cargar comentarios iniciales: {e}\n")
