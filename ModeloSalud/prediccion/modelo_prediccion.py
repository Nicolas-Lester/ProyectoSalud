# Algoritmo de prediccion de demanda de pacientes
# Usa regresion lineal multiple para predecir la cantidad de pacientes

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import joblib
import os
from datetime import datetime, timedelta
from django.conf import settings

# Ruta para guardar el modelo
MODELO_DIR = os.path.join(settings.BASE_DIR, 'modelos')
MODELO_PATH = os.path.join(MODELO_DIR, 'prediccion_demanda.joblib')
SCALER_PATH = os.path.join(MODELO_DIR, 'scaler_demanda.joblib')


# Funcion para entrenar el modelo de prediccion
def entrenar_modelo_prediccion(datos_historicos):
    """
    Entrena un modelo de regresion lineal para predecir demanda de pacientes
    
    Parametros:
    - datos_historicos: DataFrame con columnas [fecha, dia_semana, mes, pacientes, es_feriado]
    
    Retorna:
    - Diccionario con el resultado del entrenamiento
    """
    
    # Verificar que tengamos datos suficientes
    if len(datos_historicos) < 10:
        return {
            'ok': False,
            'error': 'Se necesitan al menos 10 registros historicos'
        }
    
    # Paso 1: Preparar las caracteristicas (X) y la variable objetivo (y)
    # X = variables que usamos para predecir
    # y = lo que queremos predecir (numero de pacientes)
    
    X = datos_historicos[['dia_semana', 'mes', 'es_feriado']].values
    y = datos_historicos['pacientes'].values
    
    # Paso 2: Normalizar los datos
    # Esto ayuda a que el modelo aprenda mejor
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Paso 3: Crear y entrenar el modelo de regresion lineal
    modelo = LinearRegression()
    modelo.fit(X_scaled, y)
    
    # Paso 4: Calcular que tan bueno es el modelo
    # R² score: 1.0 = perfecto, 0.0 = malo
    score = modelo.score(X_scaled, y)
    
    # Paso 5: Guardar el modelo y el scaler para usarlos despues
    os.makedirs(MODELO_DIR, exist_ok=True)
    joblib.dump(modelo, MODELO_PATH)
    joblib.dump(scaler, SCALER_PATH)
    
    return {
        'ok': True,
        'score': score,
        'coeficientes': modelo.coef_.tolist(),
        'intercepto': float(modelo.intercept_),
        'registros_usados': len(datos_historicos)
    }


# Funcion para cargar el modelo ya entrenado
def cargar_modelo_prediccion():
    """
    Carga el modelo de prediccion guardado
    
    Retorna:
    - (modelo, scaler) o (None, None) si no existe
    """
    if os.path.exists(MODELO_PATH) and os.path.exists(SCALER_PATH):
        modelo = joblib.load(MODELO_PATH)
        scaler = joblib.load(SCALER_PATH)
        return modelo, scaler
    return None, None


# Funcion para predecir demanda de pacientes
def predecir_demanda(fecha, es_feriado=False):
    """
    Predice cuantos pacientes habra en una fecha especifica
    
    Parametros:
    - fecha: objeto datetime o string 'YYYY-MM-DD'
    - es_feriado: True si es feriado, False si no
    
    Retorna:
    - Diccionario con la prediccion
    """
    
    # Cargar el modelo
    modelo, scaler = cargar_modelo_prediccion()
    
    if modelo is None:
        return {
            'ok': False,
            'error': 'El modelo no esta entrenado. Primero debes entrenar el modelo.'
        }
    
    # Convertir fecha a datetime si viene como string
    if isinstance(fecha, str):
        fecha = datetime.strptime(fecha, '%Y-%m-%d')
    
    # Extraer caracteristicas de la fecha
    dia_semana = fecha.weekday()  # 0=Lunes, 6=Domingo
    mes = fecha.month
    feriado = 1 if es_feriado else 0
    
    # Preparar los datos de entrada
    X = np.array([[dia_semana, mes, feriado]])
    X_scaled = scaler.transform(X)
    
    # Hacer la prediccion
    prediccion = modelo.predict(X_scaled)[0]
    
    # No puede haber pacientes negativos
    prediccion = max(0, round(prediccion))
    
    # Nombre del dia
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    
    return {
        'ok': True,
        'fecha': fecha.strftime('%Y-%m-%d'),
        'dia_nombre': dias[dia_semana],
        'mes': mes,
        'es_feriado': es_feriado,
        'pacientes_predichos': int(prediccion)
    }


# Funcion para generar datos de ejemplo
def generar_datos_ejemplo():
    """
    Genera datos historicos de ejemplo para entrenar el modelo
    Simula patrones realistas de demanda en un hospital
    """
    from .models import DemandaPacientes
    
    # Limpiar datos anteriores
    DemandaPacientes.objects.all().delete()
    
    # Generar 90 dias de datos (3 meses)
    fecha_inicio = datetime.now() - timedelta(days=90)
    
    for i in range(90):
        fecha = fecha_inicio + timedelta(days=i)
        dia_semana = fecha.weekday()
        mes = fecha.month
        
        # Patron de demanda:
        # - Lunes mas pacientes (30-45)
        # - Fin de semana menos pacientes (15-25)
        # - Verano (Enero-Febrero) mas demanda
        
        if dia_semana == 0:  # Lunes
            base = 40
        elif dia_semana in [5, 6]:  # Sabado, Domingo
            base = 20
        else:
            base = 30
        
        # Ajuste por mes (verano mas demanda)
        if mes in [1, 2]:  # Enero, Febrero
            base += 10
        
        # Agregar variacion aleatoria
        pacientes = base + np.random.randint(-5, 6)
        
        # Feriados tienen menos pacientes
        es_feriado = (i % 15 == 0)  # Simulamos feriados cada 15 dias
        if es_feriado:
            pacientes = int(pacientes * 0.6)
        
        DemandaPacientes.objects.create(
            fecha=fecha.date(),
            dia_semana=dia_semana,
            mes=mes,
            pacientes=max(10, pacientes),
            es_feriado=es_feriado
        )
    
    return 90  # Retorna cantidad de registros creados
