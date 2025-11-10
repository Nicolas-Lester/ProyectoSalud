import re
import os
import joblib
import pandas as pd
from django.conf import settings
import base64
from io import BytesIO

# Importar TensorFlow para la red neuronal
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

# NLTK para limpiar el texto (palabras sin valor)
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
STOPWORDS = set(stopwords.words("spanish"))  # palabras como "el", "la", "de", etc.

# Para convertir texto en numeros que entienda la IA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

# Para generar gráficos
import matplotlib
matplotlib.use('Agg')  # Backend sin interfaz gráfica
import matplotlib.pyplot as plt
import seaborn as sns

# Rutas donde se guardan el modelo y el vectorizador
MODEL_PATH = os.path.join(settings.MODELS_DIR, "sentiment_model.h5")
VEC_PATH = os.path.join(settings.MODELS_DIR, "sentiment_tfidf.joblib")


# Palabras de negacion importantes que NO debemos eliminar
NEGACIONES = {"no", "poco", "nada", "nunca", "sin", "mal", "mala", "malo", "malas", "malos",
              "pésimo", "pésima", "terrible", "horrible", "fatal"}

# Funcion para limpiar el texto de los comentarios
def limpiar_texto(texto):
    # Paso 1: Convertir todo a minusculas
    texto = texto.lower()
    
    # Paso 2: Quitar URLs (http, www)
    texto = re.sub(r"http\S+|www\S+", " ", texto)
    
    # Paso 3: Quitar simbolos raros (emojis, signos de puntuacion, etc)
    # Solo dejamos letras, numeros y espacios
    texto = re.sub(r"[^a-záéíóúñü0-9\s]", " ", texto)
    
    # Paso 4: Normalizar espacios (quitar espacios dobles)
    texto = re.sub(r"\s+", " ", texto)
    
    # Paso 5: Quitar palabras que no aportan nada (el, la, de, etc)
    # PERO mantener negaciones importantes
    palabras = texto.split()
    palabras_filtradas = [
        palabra for palabra in palabras 
        if palabra not in STOPWORDS or palabra in NEGACIONES
    ]
    
    # Devolver el texto limpio
    return " ".join(palabras_filtradas)


# Funcion principal para entrenar la red neuronal
def entrenar_modelo(df):
    # 1. Preparar los datos
    # Eliminar filas vacias
    df = df.dropna(subset=["texto", "etiqueta"]).copy()
    
    # Limpiar todos los comentarios
    df["texto_limpio"] = df["texto"].apply(limpiar_texto)
    
    # 2. Convertir texto en numeros (TF-IDF)
    # La IA no entiende palabras, solo numeros
    # max_features=5000: usa las 5000 palabras mas importantes
    # ngram_range=(1,3): analiza palabras individuales, pares y trios
    # min_df=2: ignora palabras que aparecen solo 1 vez
    vectorizador = TfidfVectorizer(max_features=5000, ngram_range=(1,3), min_df=2)
    X = vectorizador.fit_transform(df["texto_limpio"])
    
    # Guardar el vectorizador para usarlo despues
    joblib.dump(vectorizador, VEC_PATH)
    
    # 3. Preparar las etiquetas (positivo=1, negativo=0)
    y = df["etiqueta"].map({"positivo": 1, "negativo": 0}).values
    
    # 4. Dividir datos: 80% para entrenar, 20% para probar
    X_train, X_test, y_train, y_test = train_test_split(
        X.toarray(), y, test_size=0.2, random_state=42
    )
    
    # 5. Crear la red neuronal (RED MAS PROFUNDA PARA MEJOR DETECCION)
    modelo = Sequential()
    
    # Primera capa: 256 neuronas (mas capacidad de aprendizaje)
    modelo.add(Dense(256, activation="relu", input_shape=(X_train.shape[1],)))
    modelo.add(Dropout(0.4))  # Dropout mas agresivo
    
    # Segunda capa: 128 neuronas
    modelo.add(Dense(128, activation="relu"))
    modelo.add(Dropout(0.4))
    
    # Tercera capa: 64 neuronas
    modelo.add(Dense(64, activation="relu"))
    modelo.add(Dropout(0.3))
    
    # Cuarta capa: 32 neuronas
    modelo.add(Dense(32, activation="relu"))
    
    # Capa de salida: 1 neurona (positivo o negativo)
    modelo.add(Dense(1, activation="sigmoid"))
    
    # 6. Configurar el modelo
    # Adam: algoritmo de optimizacion
    # binary_crossentropy: para clasificacion binaria (2 clases)
    modelo.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )
    
    # 7. Entrenar el modelo
    # epochs=20: el modelo vera los datos 20 veces (mas entrenamiento)
    # batch_size=16: procesa 16 comentarios a la vez
    # validation_split=0.2: usa 20% de datos para validar
    modelo.fit(
        X_train, y_train,
        epochs=20,
        batch_size=16,
        validation_split=0.2,
        verbose=1
    )
    
    # 8. Guardar el modelo entrenado
    modelo.save(MODEL_PATH)
    
    # 9. Evaluar que tan bien funciona
    perdida, precision = modelo.evaluate(X_test, y_test, verbose=0)
    
    # 10. Generar predicciones para métricas y gráficos
    y_pred_prob = modelo.predict(X_test, verbose=0)
    y_pred = (y_pred_prob > 0.5).astype(int).flatten()
    
    # 11. Generar matriz de confusión
    cm = confusion_matrix(y_test, y_pred)
    
    # 12. Crear gráfico de matriz de confusión
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Negativo', 'Positivo'],
                yticklabels=['Negativo', 'Positivo'])
    plt.title('Matriz de Confusión', fontsize=16, fontweight='bold')
    plt.ylabel('Valor Real', fontsize=12)
    plt.xlabel('Predicción', fontsize=12)
    plt.tight_layout()
    
    # Guardar gráfico en memoria
    buffer_cm = BytesIO()
    plt.savefig(buffer_cm, format='png', dpi=100, bbox_inches='tight')
    buffer_cm.seek(0)
    imagen_cm = base64.b64encode(buffer_cm.read()).decode('utf-8')
    plt.close()
    
    # 13. Crear gráfico de métricas
    # Calcular métricas adicionales
    tn, fp, fn, tp = cm.ravel()
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision_metric = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1_score = 2 * (precision_metric * recall) / (precision_metric + recall) if (precision_metric + recall) > 0 else 0
    
    # Crear gráfico de barras con las métricas
    metricas = ['Precisión', 'Recall', 'F1-Score', 'Accuracy']
    valores = [precision_metric, recall, f1_score, accuracy]
    
    plt.figure(figsize=(10, 6))
    colores = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c']
    barras = plt.bar(metricas, valores, color=colores, alpha=0.7, edgecolor='black', linewidth=1.5)
    
    # Añadir valores encima de las barras
    for i, (metrica, valor) in enumerate(zip(metricas, valores)):
        plt.text(i, valor + 0.02, f'{valor:.2%}', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.title('Métricas del Modelo', fontsize=16, fontweight='bold')
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
    
    # Devolver la precision y los gráficos
    return {
        "accuracy_test": float(precision),
        "grafico_confusion": imagen_cm,
        "grafico_metricas": imagen_metricas,
        "metricas": {
            "precision": float(precision_metric),
            "recall": float(recall),
            "f1_score": float(f1_score),
            "accuracy": float(accuracy)
        }
    }


# Funcion para cargar el modelo ya entrenado
def cargar_modelo():
    # Verificar si existen los archivos del modelo
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VEC_PATH):
        return None, None
    
    # Cargar el modelo y el vectorizador
    modelo = tf.keras.models.load_model(MODEL_PATH)
    vectorizador = joblib.load(VEC_PATH)
    
    return modelo, vectorizador


# Funcion para predecir si un comentario es positivo o negativo
def predecir(texto):
    # Cargar el modelo entrenado
    modelo, vectorizador = cargar_modelo()
    
    # Si no hay modelo, mostrar error
    if modelo is None:
        return {"ok": False, "error": "Modelo no entrenado aún."}
    
    # Limpiar el texto del comentario
    texto_limpio = limpiar_texto(texto)
    
    # Convertir el texto en numeros
    X = vectorizador.transform([texto_limpio]).toarray()
    
    # Hacer la prediccion
    probabilidad = modelo.predict(X, verbose=0)[0][0]
    
    # MEJORA: Ajustar el threshold basado en palabras clave negativas
    palabras_texto = texto.lower().split()
    palabras_negativas_fuertes = ["pésimo", "pésima", "horrible", "terrible", "fatal", 
                                   "malo", "mala", "malos", "malas"]
    
    tiene_negacion_fuerte = any(palabra in palabras_negativas_fuertes for palabra in palabras_texto)
    
    # Si tiene palabras muy negativas y la probabilidad esta cerca de 0.5, forzar negativo
    if tiene_negacion_fuerte and probabilidad < 0.65:
        etiqueta = "negativo"
        probabilidad = max(0.3, probabilidad - 0.2)  # Ajustar confianza
    elif probabilidad >= 0.5:
        etiqueta = "positivo"
    else:
        etiqueta = "negativo"
    
    # Devolver el resultado
    return {
        "ok": True,
        "etiqueta": etiqueta,
        "confianza": float(probabilidad)
    }
