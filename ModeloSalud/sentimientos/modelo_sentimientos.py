import re
import os
import joblib
import pandas as pd
from django.conf import settings

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
    
    # Devolver la precision (accuracy)
    return {"accuracy_test": float(precision)}


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
