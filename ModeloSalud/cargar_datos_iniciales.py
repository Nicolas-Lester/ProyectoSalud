"""
Script de carga inicial de datos para ProyectoSalud.
Ejecuta este archivo SOLO LA PRIMERA VEZ para cargar los datos desde los CSV a PostgreSQL.

Uso:
    cd ModeloSalud
    python cargar_datos_iniciales.py
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ModeloSalud.settings')
django.setup()

import pandas as pd
from sentimientos.models import Comment
from prediccion.models import DemandaPacientes
from datetime import datetime

"""Carga comentarios de pacientes desde CSV a la base de datos."""
def cargar_comentarios():
    
    print("\n" + "="*60)
    print("CARGANDO COMENTARIOS DE PACIENTES")
    print("="*60)
    
    # Ruta al CSV (ajusta si es necesario)
    csv_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "Comentarios_de_pacientes.csv"
    )
    
    if not os.path.exists(csv_path):
        print(f"ERROR: No se encontro el archivo: {csv_path}")
        return False
    
    try:
        df = pd.read_csv(csv_path)
        print(f"   Registros en CSV: {len(df)}")
        
        contador_nuevos = 0
        contador_duplicados = 0
        
        for _, row in df.iterrows():
            texto = row.get("texto", "").strip()
            if texto:
                # Usar get_or_create para evitar duplicados
                obj, created = Comment.objects.get_or_create(
                    texto=texto,
                    defaults={
                        'fecha': row.get("fecha"),
                        'etiqueta': row.get("etiqueta", "").lower()
                    }
                )
                if created:
                    contador_nuevos += 1
                else:
                    contador_duplicados += 1
        
        print(f"   Comentarios nuevos: {contador_nuevos}")
        if contador_duplicados > 0:
            print(f"   Duplicados omitidos: {contador_duplicados}")
        print(f"   Total en BD: {Comment.objects.count()}")
        return True
    
    except Exception as e:
        print(f"   ERROR al cargar comentarios: {str(e)}")
        return False

"""Carga datos de demanda de pacientes desde CSV a la base de datos."""
def cargar_demanda():
    print("\n" + "="*60)
    print("CARGANDO DATOS DE DEMANDA DE PACIENTES")
    print("="*60)
    
    # Ruta al CSV (ajusta si es necesario)
    csv_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "Datos_Demanda_Pacientes.csv"
    )
    
    if not os.path.exists(csv_path):
        print(f"ERROR: No se encontro el archivo: {csv_path}")
        return False
    
    try:
        df = pd.read_csv(csv_path)
        print(f"   Registros en CSV: {len(df)}")
        
        contador_nuevos = 0
        contador_duplicados = 0
        
        for _, row in df.iterrows():
            fecha = datetime.strptime(row['fecha'], '%Y-%m-%d').date()
            es_feriado = str(row['es_feriado']).lower() in ['true', '1', 'yes', 'si']
            
            # Usar get_or_create para evitar duplicados
            obj, created = DemandaPacientes.objects.get_or_create(
                fecha=fecha,
                defaults={
                    'dia_semana': int(row['dia_semana']),
                    'mes': int(row['mes']),
                    'pacientes': int(row['pacientes']),
                    'es_feriado': es_feriado
                }
            )
            if created:
                contador_nuevos += 1
            else:
                contador_duplicados += 1
        
        print(f"   Registros nuevos: {contador_nuevos}")
        if contador_duplicados > 0:
            print(f"   Duplicados omitidos: {contador_duplicados}")
        print(f"   Total en BD: {DemandaPacientes.objects.count()}")
        return True
    
    except Exception as e:
        print(f"   ERROR al cargar demanda: {str(e)}")
        return False
    

"""Verifica que los datos se hayan cargado correctamente."""
def verificar_datos():
    print("\n" + "="*60)
    print("VERIFICACION DE DATOS")
    print("="*60)
    
    # Verificar comentarios
    total_comentarios = Comment.objects.count()
    print(f"   Comentarios en BD: {total_comentarios}")
    if total_comentarios > 0:
        print("   Muestra de comentarios:")
        for comentario in Comment.objects.all()[:3]:
            print(f"      - [{comentario.etiqueta}] {comentario.texto[:50]}...")
    
    # Verificar demanda
    total_demanda = DemandaPacientes.objects.count()
    print(f"\n   Registros de demanda en BD: {total_demanda}")
    if total_demanda > 0:
        print("   Muestra de registros:")
        for registro in DemandaPacientes.objects.all().order_by('fecha')[:3]:
            print(f"      - {registro.fecha}: {registro.pacientes} pacientes")
            
  """Función principal que ejecuta la carga de datos."""
def main():  
    print("\n" + "="*60)
    print("CARGA INICIAL DE DATOS - ProyectoSalud")
    print("="*60)
    print("\nEste script cargara los datos desde los archivos CSV a PostgreSQL.")
    print("Solo debes ejecutarlo UNA VEZ durante la instalacion inicial.\n")
    
    respuesta = input("Deseas continuar? (s/n): ").lower()
    if respuesta != 's':
        print("\nOperacion cancelada.")
        return
    
    # Cargar comentarios
    exito_comentarios = cargar_comentarios()
    
    # Cargar demanda
    exito_demanda = cargar_demanda()
    
    # Verificar datos
    if exito_comentarios or exito_demanda:
        verificar_datos()
    
    # Mensaje final
    print("\n" + "="*60)
    if exito_comentarios and exito_demanda:
        print("CARGA COMPLETADA EXITOSAMENTE")
        print("="*60)

    else:
        print("CARGA COMPLETADA CON ERRORES")
        print("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperacion cancelada por el usuario.")
    except Exception as e:
        print(f"\n\nERROR INESPERADO: {str(e)}")
        print("Contacta al desarrollador si el problema persiste.")
