"""
Configuración de la aplicación de predicción.
Carga automáticamente los datos iniciales del CSV si la base de datos está vacía.
"""

from django.apps import AppConfig


class PrediccionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'prediccion'
    
    def ready(self):
        """
        Este método se ejecuta automáticamente cuando Django inicia.
        Aquí cargamos los datos de demanda del CSV si la tabla está vacía.
        """
        # Solo ejecutar en el proceso principal (no en reloader)
        import os
        if os.environ.get('RUN_MAIN') != 'true':
            return
        
        # Importar aquí para evitar errores de apps no cargadas
        from prediccion.models import DemandaPacientes
        from django.core.management import call_command
        
        try:
            # Verificar si la tabla está vacía
            if DemandaPacientes.objects.count() == 0:
                print("\n" + "="*60)
                print("🔄 Primera ejecución detectada - Predicción")
                print("   Cargando datos de demanda iniciales desde CSV...")
                print("="*60 + "\n")
                
                # Llamar al comando load_demanda automáticamente
                call_command('load_demanda')
                
                print("\n" + "="*60)
                print("✅ Datos de demanda cargados correctamente")
                print("="*60 + "\n")
        
        except Exception as e:
            # Si hay error, mostrar pero no detener Django
            print(f"\n⚠️  No se pudieron cargar datos de demanda iniciales: {e}\n")
