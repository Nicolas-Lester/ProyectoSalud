"""
Comando Django para cargar datos historicos de demanda desde CSV
Uso: python manage.py load_demanda --path ruta/al/archivo.csv
"""

from django.core.management.base import BaseCommand
from prediccion.models import DemandaPacientes
import csv
from datetime import datetime


class Command(BaseCommand):
    help = 'Carga datos historicos de demanda de pacientes desde un archivo CSV'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            help='Ruta al archivo CSV con los datos historicos',
            default='../Datos_Demanda_Pacientes.csv'
        )

    def handle(self, *args, **options):
        csv_path = options['path']
        
        self.stdout.write(self.style.WARNING(f'Cargando datos desde: {csv_path}'))
        
        # Borrar datos existentes
        deleted = DemandaPacientes.objects.all().delete()
        self.stdout.write(self.style.WARNING(f'Se eliminaron {deleted[0]} registros antiguos'))
        
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
