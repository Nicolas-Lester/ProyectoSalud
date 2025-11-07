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
    palabras = texto.split()
    palabras_filtradas = [palabra for palabra in palabras if palabra not in STOPWORDS]
    
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
    vectorizador = TfidfVectorizer(min_df=1, ngram_range=(1,2))
    X = vectorizador.fit_transform(df["texto_limpio"])
    
    # Guardar el vectorizador para usarlo despues
    joblib.dump(vectorizador, VEC_PATH)
    
    # 3. Preparar las etiquetas (positivo=1, negativo=0)
    y = df["etiqueta"].map({"positivo": 1, "negativo": 0}).values
    
    # 4. Dividir datos: 80% para entrenar, 20% para probar
    X_train, X_test, y_train, y_test = train_test_split(
        X.toarray(), y, test_size=0.2, random_state=42
    )
    
    # 5. Crear la red neuronal
    modelo = Sequential()
    
    # Primera capa: 128 neuronas
    modelo.add(Dense(128, activation="relu", input_shape=(X_train.shape[1],)))
    
    # Dropout para evitar sobreajuste (apaga 30% de neuronas aleatoriamente)
    modelo.add(Dropout(0.3))
    
    # Segunda capa: 64 neuronas
    modelo.add(Dense(64, activation="relu"))
    
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
    # epochs=10: el modelo vera los datos 10 veces
    # batch_size=16: procesa 16 comentarios a la vez
    # validation_split=0.2: usa 20% de datos para validar
    modelo.fit(
        X_train, y_train,
        epochs=10,
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
    probabilidad = modelo.predict(X)[0][0]
    
    # Si la probabilidad es >= 0.5, es positivo, sino es negativo
    if probabilidad >= 0.5:
        etiqueta = "positivo"
    else:
        etiqueta = "negativo"
    
    # Devolver el resultado
    return {
        "ok": True,
        "etiqueta": etiqueta,
        "confianza": float(probabilidad)
    }
