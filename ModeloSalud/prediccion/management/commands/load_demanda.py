"""
Comando Django para cargar datos historicos de demanda desde CSV
Uso: python manage.py load_demanda --path ruta/al/archivo.csv
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from prediccion.models import DemandaPacientes
import csv
import os
from datetime import datetime


class Command(BaseCommand):
    help = 'Carga datos historicos de demanda de pacientes desde un archivo CSV (solo si está vacío)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            required=False,
            default=None,
            help='Ruta al archivo CSV (opcional, usa ruta por defecto)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Forzar carga aunque ya existan datos (BORRA datos existentes)'
        )

    def handle(self, *args, **options):
        # Verificar si ya hay datos
        total_existentes = DemandaPacientes.objects.count()
        
        if total_existentes > 0 and not options.get('force'):
            self.stdout.write(
                self.style.WARNING(
                    f"⚠️  Ya existen {total_existentes} registros en la base de datos.\n"
                    f"   No se cargará el CSV para evitar duplicados.\n"
                    f"   Usa --force para borrar y recargar."
                )
            )
            return
        
        # Ruta del CSV (por defecto busca en la raíz del proyecto)
        csv_path = options.get('path')
        if not csv_path:
            base_dir = settings.BASE_DIR.parent  # Sale de ModeloSalud/
            csv_path = os.path.join(base_dir, "Datos_Demanda_Pacientes.csv")
        
        # Verificar que existe
        if not os.path.exists(csv_path):
            self.stderr.write(
                self.style.ERROR(
                    f"❌ No se encontró el archivo CSV en: {csv_path}\n"
                    f"   Especifica la ruta con --path=\"ruta/al/archivo.csv\""
                )
            )
            return
        
        self.stdout.write(f'📂 Cargando datos desde: {csv_path}')
        
        # Si se usa --force, borrar datos existentes
        if options.get('force') and total_existentes > 0:
            deleted = DemandaPacientes.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'🗑️  Se eliminaron {deleted[0]} registros antiguos'))
        
        # Contador de registros
        contador = 0
        errores = 0
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    try:
                        # Convertir la fecha de string a objeto date
                        fecha = datetime.strptime(row['fecha'], '%Y-%m-%d').date()
                        
                        # Convertir es_feriado de string a boolean
                        es_feriado = row['es_feriado'].lower() in ['true', '1', 'yes', 'si']
                        
                        # Crear el registro en la base de datos
                        DemandaPacientes.objects.create(
                            fecha=fecha,
                            dia_semana=int(row['dia_semana']),
                            mes=int(row['mes']),
                            pacientes=int(row['pacientes']),
                            es_feriado=es_feriado
                        )
                        
                        contador += 1
                        
                        # Mostrar progreso cada 10 registros
                        if contador % 10 == 0:
                            self.stdout.write(f'  Cargados {contador} registros...')
                    
                    except Exception as e:
                        errores += 1
                        self.stdout.write(
                            self.style.ERROR(f'Error en fila {contador + errores}: {str(e)}')
                        )
            
            # Mensaje final
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✓ Proceso completado!\n'
                    f'  - Registros cargados: {contador}\n'
                    f'  - Errores: {errores}\n'
                    f'  - Total en base de datos: {DemandaPacientes.objects.count()}'
                )
            )
        
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'\n✗ No se encontro el archivo: {csv_path}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'\n✗ Error al leer el archivo: {str(e)}')
            )
