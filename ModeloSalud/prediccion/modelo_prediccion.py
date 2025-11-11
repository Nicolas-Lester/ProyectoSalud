# Modelo de prediccion de demanda de pacientes
# Este archivo contiene las funciones para predecir cuantos pacientes van a venir al hospital
# Utilizamos regresion lineal porque es simple y funciona bien para este caso

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os
from datetime import datetime, timedelta
from django.conf import settings
import base64
from io import BytesIO

# Para generar gráficos
import matplotlib
matplotlib.use('Agg')  # Backend sin interfaz gráfica
import matplotlib.pyplot as plt
import seaborn as sns

# Rutas donde guardamos los modelos entrenados
MODELO_DIR = os.path.join(settings.BASE_DIR, 'modelos')
MODELO_PATH = os.path.join(MODELO_DIR, 'prediccion_demanda.joblib')
SCALER_PATH = os.path.join(MODELO_DIR, 'scaler_demanda.joblib')


def entrenar_modelo_prediccion(datos_historicos):
    """
    Esta funcion entrena el modelo con datos historicos del hospital
    Aprende los patrones de cuantos pacientes vienen segun el dia, mes, etc.
    """
    
    # Primero verificamos que tengamos suficientes datos para entrenar
    # Si tenemos muy pocos datos, el modelo no va a aprender bien
    if len(datos_historicos) < 10:
        return {
            'ok': False,
            'error': 'Necesitamos minimo 10 dias de datos para entrenar'
        }
    
    # Preparamos los datos de entrada:
    # X son las caracteristicas que usamos (dia de la semana, mes, si es feriado)
    # y es lo que queremos predecir (cantidad de pacientes)
    X = datos_historicos[['dia_semana', 'mes', 'es_feriado']].values
    y = datos_historicos['pacientes'].values
    
    # Normalizamos los datos para que esten en la misma escala
    # Esto ayuda a que el algoritmo funcione mejor
    scaler = StandardScaler()
    X_normalizado = scaler.fit_transform(X)
    
    # Dividir datos: 80% entrenamiento, 20% prueba
    X_train, X_test, y_train, y_test = train_test_split(
        X_normalizado, y, test_size=0.2, random_state=42
    )
    
    # Creamos el modelo de regresion lineal y lo entrenamos
    modelo = LinearRegression()
    modelo.fit(X_train, y_train)
    
    # Calculamos que tan bueno es el modelo
    # El score va de 0 a 1, siendo 1 el mejor
    precision_train = modelo.score(X_train, y_train)
    precision_test = modelo.score(X_test, y_test)
    
    # Hacer predicciones en el conjunto de prueba
    y_pred = modelo.predict(X_test)
    
    # Calcular métricas adicionales
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    # Crear gráfico de predicciones vs valores reales
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.6, edgecolor='black', s=80, color='#3498db')
    
    # Línea de predicción perfecta
    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Predicción perfecta')
    
    plt.xlabel('Pacientes Reales', fontsize=12, fontweight='bold')
    plt.ylabel('Pacientes Predichos', fontsize=12, fontweight='bold')
    plt.title('Predicciones vs Valores Reales', fontsize=16, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    # Guardar gráfico en memoria
    buffer_pred = BytesIO()
    plt.savefig(buffer_pred, format='png', dpi=100, bbox_inches='tight')
    buffer_pred.seek(0)
    imagen_pred = base64.b64encode(buffer_pred.read()).decode('utf-8')
    plt.close()
    
    # Crear gráfico de métricas
    metricas_nombres = ['R² Score', 'MAE', 'RMSE']
    metricas_valores = [r2, mae, rmse]
    
    # Normalizar RMSE y MAE para visualización (como porcentaje del promedio)
    promedio_y = y.mean()
    mae_norm = 1 - (mae / promedio_y) if promedio_y > 0 else 0
    rmse_norm = 1 - (rmse / promedio_y) if promedio_y > 0 else 0
    
    metricas_vis = [r2, mae_norm, rmse_norm]
    
    plt.figure(figsize=(10, 6))
    colores = ['#2ecc71', '#e74c3c', '#f39c12']
    barras = plt.bar(metricas_nombres, metricas_vis, color=colores, alpha=0.7, edgecolor='black', linewidth=1.5)
    
    # Añadir valores encima de las barras
    for i, (metrica, valor) in enumerate(zip(metricas_nombres, metricas_valores)):
        if i == 0:  # R² Score
            plt.text(i, metricas_vis[i] + 0.02, f'{valor:.3f}', ha='center', va='bottom', fontsize=12, fontweight='bold')
        else:  # MAE y RMSE
            plt.text(i, metricas_vis[i] + 0.02, f'{valor:.2f}', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.title('Métricas del Modelo de Regresión', fontsize=16, fontweight='bold')
    plt.ylabel('Valor', fontsize=12)
    plt.ylim(0, 1.1)
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    # Guardar gráfico en memoria
    buffer_metricas = BytesIO()
    plt.savefig(buffer_metricas, format='png', dpi=100, bbox_inches='tight')
    buffer_metricas.seek(0)
    imagen_metricas = base64.b64encode(buffer_metricas.read()).decode('utf-8')
    plt.close()
    
    # Guardamos el modelo y el scaler para poder usarlos despues
    os.makedirs(MODELO_DIR, exist_ok=True)
    joblib.dump(modelo, MODELO_PATH)
    joblib.dump(scaler, SCALER_PATH)
    
    # Retornamos los resultados del entrenamiento
    return {
        'ok': True,
        'score': precision_test,
        'score_train': precision_train,
        'coeficientes': modelo.coef_.tolist(),
        'intercepto': float(modelo.intercept_),
        'registros_usados': len(datos_historicos),
        'grafico_predicciones': imagen_pred,
        'grafico_metricas': imagen_metricas,
        'metricas': {
            'r2_score': float(r2),
            'mae': float(mae),
            'rmse': float(rmse),
            'precision_train': float(precision_train),
            'precision_test': float(precision_test)
        }
    }


def cargar_modelo_prediccion():
    """
    Carga el modelo que ya entrenamos anteriormente
    Si no existe, devuelve None
    """
    if os.path.exists(MODELO_PATH) and os.path.exists(SCALER_PATH):
        modelo = joblib.load(MODELO_PATH)
        scaler = joblib.load(SCALER_PATH)
        return modelo, scaler
    return None, None


def predecir_demanda(fecha, es_feriado=False):
    """
    Esta es la funcion principal que predice cuantos pacientes vendran
    Le pasamos una fecha y nos dice cuantos pacientes esperar
    """
    
    # Intentamos cargar el modelo entrenado
    modelo, scaler = cargar_modelo_prediccion()
    
    if modelo is None:
        return {
            'ok': False,
            'error': 'Primero hay que entrenar el modelo con datos historicos'
        }
    
    # Si la fecha viene como texto, la convertimos a formato de fecha
    if isinstance(fecha, str):
        fecha = datetime.strptime(fecha, '%Y-%m-%d')
    
    # Extraemos la informacion que necesitamos de la fecha
    dia_semana = fecha.weekday()  # 0 = Lunes, 6 = Domingo
    mes = fecha.month  # Numero del mes (1-12)
    feriado = 1 if es_feriado else 0
    
    # Preparamos los datos igual que cuando entrenamos
    X = np.array([[dia_semana, mes, feriado]])
    X_normalizado = scaler.transform(X)
    
    # Hacemos la prediccion!
    prediccion = modelo.predict(X_normalizado)[0]
    
    # Redondeamos y nos aseguramos que no sea negativo
    prediccion = max(0, round(prediccion))
    
    # Lista con los nombres de los dias para mostrar mejor
    dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    
    # Devolvemos toda la informacion de la prediccion
    return {
        'ok': True,
        'fecha': fecha.strftime('%Y-%m-%d'),
        'dia_nombre': dias_semana[dia_semana],
        'mes': mes,
        'es_feriado': es_feriado,
        'pacientes_predichos': int(prediccion)
    }


def generar_datos_ejemplo():
    """
    Genera datos de ejemplo para poder probar el modelo
    Simula 90 dias de datos historicos con patrones realistas
    """
    from .models import DemandaPacientes
    
    # Borramos los datos viejos para empezar de nuevo
    DemandaPacientes.objects.all().delete()
    
    # Vamos a generar datos de los ultimos 90 dias
    fecha_inicio = datetime.now() - timedelta(days=90)
    
    for i in range(90):
        fecha = fecha_inicio + timedelta(days=i)
        dia_semana = fecha.weekday()
        mes = fecha.month
        
        # Definimos cuantos pacientes base segun el dia
        # Los lunes suele haber mas pacientes (acumulacion del fin de semana)
        # Los fines de semana hay menos pacientes
        if dia_semana == 0:  # Lunes
            pacientes_base = 40
        elif dia_semana in [5, 6]:  # Sabado y Domingo
            pacientes_base = 20
        else:  # Martes a Viernes
            pacientes_base = 30
        
        # En verano (Enero y Febrero) hay mas demanda
        if mes in [1, 2]:
            pacientes_base += 10
        
        # Agregamos un poco de variacion aleatoria para que sea mas realista
        variacion = np.random.randint(-5, 6)
        pacientes = pacientes_base + variacion
        
        # Simulamos feriados cada 15 dias aproximadamente
        # En feriados hay menos pacientes (60% de lo normal)
        es_feriado = (i % 15 == 0)
        if es_feriado:
            pacientes = int(pacientes * 0.6)
        
        # Guardamos el registro en la base de datos
        # Nos aseguramos que haya minimo 10 pacientes
        DemandaPacientes.objects.create(
            fecha=fecha.date(),
            dia_semana=dia_semana,
            mes=mes,
            pacientes=max(10, pacientes),
            es_feriado=es_feriado
        )
    
    return 90  # Retornamos cuantos registros creamos

