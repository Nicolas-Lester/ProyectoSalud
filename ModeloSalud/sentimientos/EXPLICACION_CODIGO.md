# 💬 Explicación de la Implementación del Análisis de Sentimientos

## 📋 Índice
1. [Introducción](#introducción)
2. [Librerías Utilizadas](#librerías-utilizadas)
3. [Preprocesamiento de Texto](#preprocesamiento-de-texto)
4. [Función de Entrenamiento](#función-de-entrenamiento)
5. [Arquitectura de la Red Neuronal](#arquitectura-de-la-red-neuronal)
6. [Función de Predicción](#función-de-predicción)
7. [Decisiones de Diseño](#decisiones-de-diseño)
8. [Flujo Completo](#flujo-completo)

---

## 🎯 Introducción

Este módulo implementa un **clasificador de sentimientos** usando **Deep Learning** (Redes Neuronales Artificiales) con TensorFlow/Keras. Analiza comentarios de pacientes y determina si son **positivos** o **negativos**.

**Archivo:** `modelo_sentimientos.py`

**Tecnologías:**
- 🧠 **TensorFlow/Keras** - Red neuronal profunda
- 📊 **TF-IDF** - Vectorización de texto
- 🧹 **NLTK** - Limpieza de texto en español
- 📈 **Matplotlib/Seaborn** - Visualización de resultados

---

## 📚 Librerías Utilizadas

### **1. Procesamiento de Texto**

```python
import re
import nltk
from nltk.corpus import stopwords
```

#### **re (Regular Expressions)**
**¿Qué hace?**
- Módulo para trabajar con expresiones regulares
- Permite buscar, reemplazar y limpiar patrones en texto

**Funciones utilizadas:**

##### `re.sub(patrón, reemplazo, texto)`
```python
# Eliminar URLs
texto = re.sub(r"http\S+|www\S+", " ", texto)
# Si texto = "Visita www.ejemplo.com para más"
# Resultado: "Visita   para más"

# Eliminar símbolos especiales
texto = re.sub(r"[^a-záéíóúñü0-9\s]", " ", texto)
# Si texto = "¡Excelente! Muy bueno :)"
# Resultado: "Excelente  Muy bueno  "
```

**¿Por qué usamos regex?**
- ✅ Eficiente para limpiar grandes cantidades de texto
- ✅ Flexible: un patrón puede limpiar muchos casos
- ✅ Estandarizado: funciona igual en cualquier texto

---

#### **NLTK (Natural Language Toolkit)**
**¿Qué es?**
- Librería especializada en procesamiento de lenguaje natural
- Incluye diccionarios, corpus y herramientas lingüísticas

```python
nltk.download('stopwords')
STOPWORDS = set(stopwords.words("spanish"))
```

**¿Qué son stopwords?**
- Palabras comunes que **no aportan significado** para clasificar sentimientos
- Ejemplos: "el", "la", "de", "que", "en", "y", etc.

**¿Por qué eliminarlas?**
- ✅ Reducen ruido en el modelo
- ✅ El modelo se enfoca en palabras importantes
- ✅ Mejora la precisión y velocidad

**Ejemplo:**
```python
STOPWORDS = {'el', 'la', 'de', 'que', 'en', 'y', 'un', 'por', ...}

texto_original = "el servicio fue muy bueno y la atención excelente"
# Después de quitar stopwords:
# "servicio fue muy bueno atención excelente"
```

**¿Por qué usamos `set()`?**
- Las búsquedas en un set son O(1) (instantáneas)
- Más rápido que buscar en una lista

---

### **2. Machine Learning**

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
```

#### **TfidfVectorizer**
**¿Qué hace?**
Convierte texto en números que la red neuronal puede entender.

**TF-IDF = Term Frequency - Inverse Document Frequency**

**Fórmula:**
```
TF-IDF(palabra) = (Frecuencia en el documento) × log(Total documentos / Documentos con la palabra)
```

**Ejemplo práctico:**
```python
comentarios = [
    "excelente servicio rápido",
    "muy malo servicio lento",
    "excelente atención"
]

vectorizador = TfidfVectorizer()
X = vectorizador.fit_transform(comentarios)

# Resultado (simplificado):
#              excelente  servicio  rápido  malo  lento  atención
# Comentario 1:   0.58      0.42     0.58    0.0   0.0     0.0
# Comentario 2:   0.0       0.35     0.0     0.60  0.60    0.0
# Comentario 3:   0.71      0.0      0.0     0.0   0.0     0.71
```

**¿Por qué TF-IDF?**
- ✅ Palabras frecuentes tienen menos peso ("servicio" aparece mucho)
- ✅ Palabras únicas tienen más peso ("excelente" es más distintiva)
- ✅ Funciona muy bien para clasificación de texto

**Parámetros en nuestro código:**
```python
TfidfVectorizer(max_features=5000, ngram_range=(1,3), min_df=2)
```

- `max_features=5000`: Usa solo las 5000 palabras más importantes
- `ngram_range=(1,3)`: Analiza palabras solas, pares y tríos
- `min_df=2`: Ignora palabras que aparecen solo 1 vez

**¿Qué son n-grams?**
```python
texto = "muy buen servicio"

# 1-grams (palabras individuales):
["muy", "buen", "servicio"]

# 2-grams (pares):
["muy buen", "buen servicio"]

# 3-grams (tríos):
["muy buen servicio"]
```

**¿Por qué usar n-grams?**
- "muy bueno" tiene diferente significado que "bueno" solo
- "no recomiendo" es diferente a "recomiendo"
- Captura contexto y negaciones

---

#### **train_test_split**
```python
X_train, X_test, y_train, y_test = train_test_split(
    X.toarray(), y, test_size=0.2, random_state=42
)
```

**¿Qué hace?**
Divide los datos en **entrenamiento** (80%) y **prueba** (20%)

**Visualización:**
```
Datos totales: 100 comentarios
    ↓
    ├─ 80 comentarios → Entrenamiento (el modelo aprende con estos)
    └─ 20 comentarios → Prueba (evaluamos qué tan bien aprendió)
```

**¿Por qué dividir?**
- ✅ **Entrenamiento:** El modelo aprende patrones
- ✅ **Prueba:** Verificamos si funciona con datos nuevos
- ✅ Evita **overfitting** (memorizar en lugar de aprender)

**Parámetros:**
- `test_size=0.2`: 20% para prueba
- `random_state=42`: Número para reproducibilidad (siempre la misma división)

---

### **3. Deep Learning**

```python
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
```

#### **TensorFlow/Keras**
**¿Qué es?**
- Librería de Google para crear redes neuronales
- Keras es la API de alto nivel (más fácil de usar)

#### **Sequential**
**¿Qué es?**
Modelo que apila capas una tras otra (secuencialmente)

```python
modelo = Sequential()
# Capa 1
modelo.add(Dense(...))
# Capa 2
modelo.add(Dense(...))
# Capa 3
modelo.add(Dense(...))
```

#### **Dense (Capa Densa)**
**¿Qué es?**
Capa donde todas las neuronas están conectadas entre sí.

```python
modelo.add(Dense(256, activation="relu", input_shape=(5000,)))
```

**Parámetros:**
- `256`: Número de neuronas en esta capa
- `activation="relu"`: Función de activación (más sobre esto después)
- `input_shape=(5000,)`: El input tiene 5000 características (palabras)

**Visualización:**
```
Input (5000 palabras)
    ↓
[Neurona 1] ←─┐
[Neurona 2] ←─┤
[Neurona 3] ←─┼─ Todas conectadas a todas
    ...      │
[Neurona 256]←─┘
    ↓
Siguiente capa
```

#### **Dropout**
**¿Qué hace?**
Apaga aleatoriamente algunas neuronas durante el entrenamiento.

```python
modelo.add(Dropout(0.4))  # Apaga 40% de neuronas
```

**¿Por qué?**
- ✅ Evita **overfitting** (memorizar)
- ✅ Fuerza al modelo a aprender patrones generales
- ✅ Hace la red más robusta

**Analogía:**
```
Estudiar para un examen:
- Sin Dropout: Memorizar las respuestas exactas
- Con Dropout: Entender los conceptos (funciona con preguntas nuevas)
```

---

### **4. Visualización**

```python
import matplotlib.pyplot as plt
import seaborn as sns
```

#### **Matplotlib**
Librería para crear gráficos.

```python
matplotlib.use('Agg')  # Sin interfaz gráfica (para servidor)
```

**¿Por qué `Agg`?**
- Genera imágenes sin mostrarlas en pantalla
- Perfecto para aplicaciones web (Django)

#### **Seaborn**
Librería de visualización basada en Matplotlib (más bonita).

```python
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
```

Crea mapas de calor con colores según los valores.

---

## 🧹 Preprocesamiento de Texto

### **Función `limpiar_texto()`**

```python
def limpiar_texto(texto):
```

Esta función **limpia y normaliza** el texto antes de procesarlo.

---

#### **PASO 1: Convertir a minúsculas**

```python
texto = texto.lower()
```

**¿Por qué?**
- "Excelente" y "excelente" son la misma palabra
- Reduce vocabulario y mejora el aprendizaje

**Ejemplo:**
```python
texto = "El Servicio Fue EXCELENTE"
texto = texto.lower()
# Resultado: "el servicio fue excelente"
```

---

#### **PASO 2: Eliminar URLs**

```python
texto = re.sub(r"http\S+|www\S+", " ", texto)
```

**¿Qué hace?**
Elimina cualquier URL del texto.

**Patrón regex explicado:**
- `http\S+`: Cualquier cosa que empiece con "http" y no tenga espacios
- `|`: O
- `www\S+`: Cualquier cosa que empiece con "www" y no tenga espacios

**Ejemplo:**
```python
texto = "Visita www.hospital.com para más info"
texto = re.sub(r"http\S+|www\S+", " ", texto)
# Resultado: "Visita   para más info"
```

**¿Por qué eliminar URLs?**
- No aportan sentimiento
- Son ruido para el modelo

---

#### **PASO 3: Eliminar símbolos especiales**

```python
texto = re.sub(r"[^a-záéíóúñü0-9\s]", " ", texto)
```

**¿Qué hace?**
Elimina TODO excepto letras, números y espacios.

**Patrón regex explicado:**
- `[^...]`: Negación (todo lo que NO esté en la lista)
- `a-z`: Letras minúsculas
- `áéíóúñü`: Letras con acentos y ñ
- `0-9`: Números
- `\s`: Espacios

**Ejemplo:**
```python
texto = "¡Excelente! Muy bueno :) #salud"
texto = re.sub(r"[^a-záéíóúñü0-9\s]", " ", texto)
# Resultado: " Excelente  Muy bueno    salud"
```

**¿Por qué?**
- Emojis y símbolos pueden confundir al modelo
- Estandariza el formato del texto

---

#### **PASO 4: Normalizar espacios**

```python
texto = re.sub(r"\s+", " ", texto)
```

**¿Qué hace?**
Reemplaza múltiples espacios consecutivos por uno solo.

**Ejemplo:**
```python
texto = "excelente    muy    bueno"
texto = re.sub(r"\s+", " ", texto)
# Resultado: "excelente muy bueno"
```

---

#### **PASO 5: Eliminar stopwords (pero conservar negaciones)**

```python
palabras = texto.split()
palabras_filtradas = [
    palabra for palabra in palabras 
    if palabra not in STOPWORDS or palabra in NEGACIONES
]
return " ".join(palabras_filtradas)
```

**¿Qué hace línea por línea?**

**Línea 1:** Dividir texto en palabras
```python
texto = "el servicio fue muy bueno"
palabras = texto.split()
# ['el', 'servicio', 'fue', 'muy', 'bueno']
```

**Línea 2-5:** List comprehension (filtro)
```python
palabras_filtradas = [
    palabra for palabra in palabras 
    if palabra not in STOPWORDS or palabra in NEGACIONES
]
```

**Desglose de la condición:**
```python
if palabra not in STOPWORDS or palabra in NEGACIONES
#  ↑ Condición A           ↑ Condición B
```

- **Condición A:** La palabra NO es stopword → MANTENER
- **Condición B:** La palabra ES negación → MANTENER (especial)
- **Lógica `or`:** Si CUALQUIERA es True, mantener la palabra

**¿Por qué conservar negaciones?**
```python
NEGACIONES = {"no", "poco", "nada", "nunca", "sin", "mal", 
              "mala", "malo", "pésimo", "terrible", "horrible"}
```

Las negaciones **cambian completamente el sentimiento**:
- "bueno" → POSITIVO
- "no bueno" → NEGATIVO

**Ejemplo completo:**
```python
texto = "el servicio no fue muy bueno"
palabras = ['el', 'servicio', 'no', 'fue', 'muy', 'bueno']

# 'el' → stopword → ELIMINAR
# 'servicio' → NO stopword → MANTENER
# 'no' → stopword PERO negación → MANTENER
# 'fue' → stopword → ELIMINAR
# 'muy' → stopword → ELIMINAR
# 'bueno' → NO stopword → MANTENER

palabras_filtradas = ['servicio', 'no', 'bueno']
```

**Línea 6:** Unir las palabras de nuevo
```python
return " ".join(palabras_filtradas)
# "servicio no bueno"
```

---

### **Ejemplo Completo de `limpiar_texto()`**

```python
texto_original = "¡El servicio fue EXCELENTE! www.hospital.com :)"

# Paso 1: Minúsculas
# "¡el servicio fue excelente! www.hospital.com :)"

# Paso 2: Quitar URLs
# "¡el servicio fue excelente!  :)"

# Paso 3: Quitar símbolos
# " el servicio fue excelente   "

# Paso 4: Normalizar espacios
# " el servicio fue excelente "

# Paso 5: Quitar stopwords
# "servicio excelente"

texto_limpio = "servicio excelente"
```

---

## 🎓 Función de Entrenamiento

### **`entrenar_modelo(df)`**

Esta es la función **más importante**. Entrena la red neuronal con los comentarios.

**Parámetro:**
- `df` (DataFrame): Tabla con columnas `texto` y `etiqueta`

---

### **PARTE 1: Preparar los Datos**

```python
# 1. Eliminar filas vacías
df = df.dropna(subset=["texto", "etiqueta"]).copy()
```

**¿Qué hace `dropna()`?**
Elimina filas donde `texto` o `etiqueta` están vacías (NaN, None, "")

**¿Por qué `.copy()`?**
Crea una copia para evitar modificar el DataFrame original.

---

```python
# 2. Limpiar todos los comentarios
df["texto_limpio"] = df["texto"].apply(limpiar_texto)
```

**¿Qué hace `apply()`?**
Aplica una función a cada elemento de una columna.

**Equivalente con bucle:**
```python
# apply() hace esto automáticamente:
for i in range(len(df)):
    df.loc[i, "texto_limpio"] = limpiar_texto(df.loc[i, "texto"])
```

**Resultado:**
```
DataFrame antes:
| texto                          | etiqueta  |
|--------------------------------|-----------|
| "¡Excelente servicio!"         | positivo  |
| "Muy mal, no recomiendo"       | negativo  |

DataFrame después:
| texto                          | etiqueta  | texto_limpio         |
|--------------------------------|-----------|----------------------|
| "¡Excelente servicio!"         | positivo  | "excelente servicio" |
| "Muy mal, no recomiendo"       | negativo  | "mal no recomiendo"  |
```

---

### **PARTE 2: Vectorización TF-IDF**

```python
vectorizador = TfidfVectorizer(max_features=5000, ngram_range=(1,3), min_df=2)
X = vectorizador.fit_transform(df["texto_limpio"])
```

**¿Qué hace `fit_transform()`?**
1. **`fit`:** Aprende el vocabulario (qué palabras existen)
2. **`transform`:** Convierte los textos en vectores numéricos

**Ejemplo:**
```python
textos = [
    "servicio excelente rápido",
    "servicio malo lento",
    "atención excelente"
]

vectorizador = TfidfVectorizer()
X = vectorizador.fit_transform(textos)

# vocabulario aprendido: 
# ['atención', 'excelente', 'lento', 'malo', 'rápido', 'servicio']

# X = matriz numérica (3 textos × 6 palabras)
```

**¿Por qué `.toarray()` después?**
```python
X_train, X_test, y_train, y_test = train_test_split(
    X.toarray(), y, test_size=0.2, random_state=42
)
```

TF-IDF devuelve una matriz "sparse" (esparsa) para ahorrar memoria. La convertimos a array normal para Keras.

---

```python
joblib.dump(vectorizador, VEC_PATH)
```

**¿Qué hace `joblib.dump()`?**
Guarda el vectorizador en un archivo.

**¿Por qué guardarlo?**
- ✅ Lo necesitamos después para predecir comentarios nuevos
- ✅ Debe usar el **mismo vocabulario** que en el entrenamiento
- ✅ Si no lo guardamos, no podemos hacer predicciones

---

### **PARTE 3: Preparar Etiquetas**

```python
y = df["etiqueta"].map({"positivo": 1, "negativo": 0}).values
```

**¿Qué hace `map()`?**
Reemplaza valores según un diccionario.

**Ejemplo:**
```python
etiquetas = ["positivo", "negativo", "positivo", "negativo"]
y = pd.Series(etiquetas).map({"positivo": 1, "negativo": 0})
# y = [1, 0, 1, 0]
```

**¿Por qué convertir a números?**
- Las redes neuronales solo entienden números
- 1 = positivo, 0 = negativo
- La capa de salida usará sigmoid (0 a 1)

**¿Qué hace `.values`?**
Convierte la Serie de pandas a un array de NumPy (formato que Keras necesita).

---

### **PARTE 4: Dividir Datos**

```python
X_train, X_test, y_train, y_test = train_test_split(
    X.toarray(), y, test_size=0.2, random_state=42
)
```

**Resultado:**
```python
# Si tenemos 100 comentarios:
X_train: 80 comentarios vectorizados (para entrenar)
X_test:  20 comentarios vectorizados (para probar)
y_train: 80 etiquetas (1 o 0)
y_test:  20 etiquetas (1 o 0)
```

---

## 🧠 Arquitectura de la Red Neuronal

### **Crear el Modelo**

```python
modelo = Sequential()
```

Crea un modelo vacío donde agregaremos capas.

---

### **CAPA 1: Entrada + Primera Capa Oculta**

```python
modelo.add(Dense(256, activation="relu", input_shape=(X_train.shape[1],)))
modelo.add(Dropout(0.4))
```

#### **Dense(256, activation="relu", input_shape=...)**

**Parámetros:**
- `256`: Número de neuronas
- `activation="relu"`: Función de activación
- `input_shape=(5000,)`: Tamaño del input (5000 palabras)

**¿Qué es ReLU?**
```
ReLU(x) = max(0, x)

Si x < 0 → salida = 0
Si x ≥ 0 → salida = x
```

**Gráfica:**
```
  salida
    ↑
    |     /
    |    /
    |   /
    |__/________→ entrada
    0
```

**¿Por qué ReLU?**
- ✅ Simple y rápida
- ✅ Evita el "vanishing gradient" (problema de redes profundas)
- ✅ Funciona muy bien en la práctica

#### **Dropout(0.4)**
Apaga aleatoriamente 40% de las neuronas.

**Visualización:**
```
Entrenamiento (con Dropout):
[●] [○] [●] [○] [●] [●] [○] [●] ...
 ↑   ↑   ↑   ↑
act. off act. off  (40% apagadas)

Predicción (sin Dropout):
[●] [●] [●] [●] [●] [●] [●] [●] ...
(todas activas)
```

---

### **CAPAS 2, 3 y 4: Capas Ocultas**

```python
# Segunda capa: 128 neuronas
modelo.add(Dense(128, activation="relu"))
modelo.add(Dropout(0.4))

# Tercera capa: 64 neuronas
modelo.add(Dense(64, activation="relu"))
modelo.add(Dropout(0.3))

# Cuarta capa: 32 neuronas
modelo.add(Dense(32, activation="relu"))
```

**Patrón: Pirámide invertida**
```
Input: 5000 características
    ↓
Capa 1: 256 neuronas
    ↓
Capa 2: 128 neuronas
    ↓
Capa 3: 64 neuronas
    ↓
Capa 4: 32 neuronas
    ↓
Salida: 1 neurona
```

**¿Por qué reducir gradualmente?**
- Cada capa aprende representaciones más abstractas
- Capa 1: Detecta palabras y patrones simples
- Capa 2: Combina palabras (frases)
- Capa 3: Entiende contexto
- Capa 4: Representa el sentimiento general

---

### **CAPA DE SALIDA**

```python
modelo.add(Dense(1, activation="sigmoid"))
```

**Parámetros:**
- `1`: Solo 1 neurona (clasificación binaria: positivo/negativo)
- `activation="sigmoid"`: Función que da valores entre 0 y 1

**¿Qué es Sigmoid?**
```
Sigmoid(x) = 1 / (1 + e^(-x))

Rango: 0 a 1
```

**Gráfica:**
```
  salida
   1 |        ___________
     |      /
   0.5|    /
     |   /
   0 |__/_____________→ entrada
```

**Interpretación:**
```
Salida = 0.8 → 80% seguro que es POSITIVO
Salida = 0.2 → 20% seguro que es positivo = 80% NEGATIVO
Salida = 0.5 → No está seguro (umbral)
```

---

### **Arquitectura Completa Visualizada**

```
Input: [5000 palabras]
         ↓
┌─────────────────────┐
│  Capa 1: 256 ReLU   │
│  Dropout 40%        │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  Capa 2: 128 ReLU   │
│  Dropout 40%        │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  Capa 3: 64 ReLU    │
│  Dropout 30%        │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  Capa 4: 32 ReLU    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  Salida: 1 Sigmoid  │
│  (0 a 1)            │
└─────────────────────┘
         ↓
    [Probabilidad]
```

---

### **COMPILAR EL MODELO**

```python
modelo.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)
```

#### **optimizer="adam"**
**¿Qué es?**
Algoritmo que ajusta los pesos de la red para minimizar el error.

**Adam = Adaptive Moment Estimation**
- Combina lo mejor de otros optimizadores
- Aprende rápido al inicio, se refina al final
- Es el más usado actualmente

**Analogía:**
```
Buscar el mejor camino en una montaña:
- SGD: Caminar paso a paso cuesta abajo
- Adam: Caminar cuesta abajo con "memoria" (más inteligente)
```

#### **loss="binary_crossentropy"**
**¿Qué es?**
Función que mide qué tan equivocado está el modelo.

**Binary Crossentropy:**
```
Loss = -[y × log(ŷ) + (1-y) × log(1-ŷ)]

y = etiqueta real (0 o 1)
ŷ = predicción del modelo (0 a 1)
```

**Ejemplo:**
```python
# Real: positivo (y=1)
# Modelo predice: 0.9

Loss = -[1 × log(0.9) + 0 × log(0.1)]
     = -log(0.9)
     ≈ 0.105 (bajo = bueno)

# Real: positivo (y=1)
# Modelo predice: 0.1

Loss = -[1 × log(0.1) + 0 × log(0.9)]
     = -log(0.1)
     ≈ 2.30 (alto = malo)
```

**¿Por qué esta función?**
- ✅ Penaliza mucho las predicciones muy incorrectas
- ✅ Recompensa predicciones correctas y confiadas
- ✅ Estándar para clasificación binaria

#### **metrics=["accuracy"]**
Métrica adicional para monitorear durante el entrenamiento.

**Accuracy (Precisión):**
```
Accuracy = Correctas / Total

Si de 100 predicciones, 85 son correctas:
Accuracy = 85 / 100 = 0.85 = 85%
```

---

### **ENTRENAR EL MODELO**

```python
modelo.fit(
    X_train, y_train,
    epochs=20,
    batch_size=16,
    validation_split=0.2,
    verbose=1
)
```

#### **Parámetros:**

**`epochs=20`**
- El modelo verá **todos** los datos 20 veces
- Cada epoch = una pasada completa por los datos

**Analogía:**
```
Estudiar para un examen:
- Epoch 1: Primera lectura del material
- Epoch 2: Segunda lectura (entiendes más)
- ...
- Epoch 20: Vigésima lectura (dominas el tema)
```

**`batch_size=16`**
- Procesa 16 comentarios a la vez antes de actualizar pesos
- Más pequeño = más actualizaciones = aprende detalles
- Más grande = menos actualizaciones = aprende patrones generales

**Proceso:**
```
Tenemos 80 comentarios de entrenamiento:

Batch 1: Comentarios 1-16   → Calcular error → Actualizar pesos
Batch 2: Comentarios 17-32  → Calcular error → Actualizar pesos
Batch 3: Comentarios 33-48  → Calcular error → Actualizar pesos
Batch 4: Comentarios 49-64  → Calcular error → Actualizar pesos
Batch 5: Comentarios 65-80  → Calcular error → Actualizar pesos

= 1 epoch completo
```

**`validation_split=0.2`**
- Usa 20% de los datos de entrenamiento para validación
- **Validación:** Evaluar el modelo durante el entrenamiento (no después)

**División:**
```
Datos originales: 100 comentarios
    ↓
Entrenamiento: 80 comentarios
    ├─ Para entrenar: 64 comentarios (80%)
    └─ Para validar: 16 comentarios (20%)
Prueba: 20 comentarios
```

**¿Por qué validación?**
- Detectar **overfitting** temprano
- Ver si el modelo generaliza bien
- Decidir cuándo parar el entrenamiento

**`verbose=1`**
- Muestra progreso en la consola
- verbose=0: sin output
- verbose=1: barra de progreso
- verbose=2: una línea por epoch

**Ejemplo de output:**
```
Epoch 1/20
5/5 [==============================] - 2s - loss: 0.6234 - accuracy: 0.7000 - val_loss: 0.5892 - val_accuracy: 0.7500
Epoch 2/20
5/5 [==============================] - 1s - loss: 0.5421 - accuracy: 0.7625 - val_loss: 0.5123 - val_accuracy: 0.8125
...
```

---

### **GUARDAR EL MODELO**

```python
modelo.save(MODEL_PATH)
```

**¿Qué hace?**
Guarda toda la red neuronal en un archivo `.h5`:
- Arquitectura (capas, neuronas)
- Pesos entrenados
- Configuración del optimizador

**¿Por qué guardar?**
- No queremos entrenar cada vez que hacemos una predicción
- Entrenar toma tiempo (minutos/horas)
- Predecir con modelo guardado es instantáneo

---

### **EVALUAR EL MODELO**

```python
perdida, precision = modelo.evaluate(X_test, y_test, verbose=0)
```

**¿Qué hace `evaluate()`?**
Prueba el modelo con datos que **nunca** ha visto.

**Retorna:**
- `perdida`: Valor de la función de pérdida (loss)
- `precision`: Accuracy (% de aciertos)

**Ejemplo:**
```python
# 20 comentarios de prueba
# Modelo acierta 17

precision = 17 / 20 = 0.85 = 85%
```

---

### **GENERAR PREDICCIONES**

```python
y_pred_prob = modelo.predict(X_test, verbose=0)
y_pred = (y_pred_prob > 0.5).astype(int).flatten()
```

**Línea 1:** Obtener probabilidades
```python
y_pred_prob = [[0.85], [0.23], [0.91], [0.12], ...]
# Cada valor es la probabilidad de ser POSITIVO
```

**Línea 2:** Convertir a etiquetas (0 o 1)
```python
y_pred_prob > 0.5
# [True, False, True, False, ...]

.astype(int)
# [1, 0, 1, 0, ...]

.flatten()
# Aplanar array de [[1], [0], [1]] a [1, 0, 1]
```

**Umbral 0.5:**
```
Probabilidad ≥ 0.5 → Positivo (1)
Probabilidad < 0.5 → Negativo (0)
```

---

### **MATRIZ DE CONFUSIÓN**

```python
cm = confusion_matrix(y_test, y_pred)
```

**¿Qué es?**
Tabla que muestra aciertos y errores del modelo.

**Estructura:**
```
                Predicción
                Neg   Pos
Real  Neg  [  TN  |  FP  ]
      Pos  [  FN  |  TP  ]

TN = True Negative (correcto: predijo negativo, era negativo)
FP = False Positive (error: predijo positivo, era negativo)
FN = False Negative (error: predijo negativo, era positivo)
TP = True Positive (correcto: predijo positivo, era positivo)
```

**Ejemplo:**
```python
cm = [[8, 2],
      [1, 9]]

# 8 negativos correctos
# 2 falsos positivos (dijo positivo, era negativo)
# 1 falso negativo (dijo negativo, era positivo)
# 9 positivos correctos
```

**Métricas calculadas:**
```python
tn, fp, fn, tp = cm.ravel()

accuracy = (tp + tn) / (tp + tn + fp + fn)
# (9 + 8) / 20 = 17/20 = 85%

precision = tp / (tp + fp)
# 9 / (9 + 2) = 9/11 = 82%

recall = tp / (tp + fn)
# 9 / (9 + 1) = 9/10 = 90%

f1_score = 2 × (precision × recall) / (precision + recall)
# 2 × (0.82 × 0.90) / (0.82 + 0.90) = 86%
```

---

### **VISUALIZACIÓN**

```python
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
```

**Parámetros:**
- `annot=True`: Mostrar números en cada celda
- `fmt='d'`: Formato entero (sin decimales)
- `cmap='Blues'`: Escala de colores azules

**Guardar en memoria (no en archivo):**
```python
buffer_cm = BytesIO()
plt.savefig(buffer_cm, format='png')
buffer_cm.seek(0)
imagen_cm = base64.b64encode(buffer_cm.read()).decode('utf-8')
```

**¿Por qué `BytesIO`?**
- Guarda la imagen en memoria (RAM)
- No crea archivos en el disco
- Perfecto para web (enviar imagen directamente)

**¿Por qué `base64.b64encode`?**
- Convierte la imagen binaria a texto
- Se puede insertar directamente en HTML
- `<img src="data:image/png;base64,{imagen_cm}">`

---

## 🔮 Función de Predicción

### **`cargar_modelo()`**

```python
def cargar_modelo():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VEC_PATH):
        return None, None
    
    modelo = tf.keras.models.load_model(MODEL_PATH)
    vectorizador = joblib.load(VEC_PATH)
    
    return modelo, vectorizador
```

**¿Qué hace?**
1. Verifica que existan los archivos guardados
2. Carga el modelo y vectorizador
3. Los retorna para usarlos

**¿Por qué verificar primero?**
- Si no existe el archivo, `load()` daría error
- Mejor retornar `None` y manejar el error elegantemente

---

### **`predecir(texto)`**

```python
def predecir(texto):
```

Esta función **predice el sentimiento** de un comentario nuevo.

---

#### **PASO 1: Cargar el Modelo**

```python
modelo, vectorizador = cargar_modelo()

if modelo is None:
    return {"ok": False, "error": "Modelo no entrenado aún."}
```

Si no hay modelo, retornar error.

---

#### **PASO 2: Limpiar el Texto**

```python
texto_limpio = limpiar_texto(texto)
```

Aplicar el mismo preprocesamiento que en el entrenamiento.

**Ejemplo:**
```python
texto = "¡El servicio fue EXCELENTE!"
texto_limpio = "servicio excelente"
```

---

#### **PASO 3: Vectorizar**

```python
X = vectorizador.transform([texto_limpio]).toarray()
```

**¿Por qué `transform()` y no `fit_transform()`?**
- `fit_transform()`: Aprende vocabulario + transforma (entrenamiento)
- `transform()`: Solo transforma usando vocabulario ya aprendido (predicción)

**¿Por qué `[texto_limpio]` con corchetes?**
- `transform()` espera una lista de textos
- Aunque sea uno solo, debe estar en lista: `["texto"]`

**Resultado:**
```python
X = [[0.0, 0.58, 0.0, 0.71, ..., 0.0]]
# Array con 5000 valores (uno por palabra del vocabulario)
```

---

#### **PASO 4: Predecir**

```python
probabilidad = modelo.predict(X, verbose=0)[0][0]
```

**Desglose:**
```python
resultado = modelo.predict(X, verbose=0)
# resultado = [[0.85]]  (array 2D)

[0]
# [0.85]  (primer elemento, array 1D)

[0]
# 0.85  (valor escalar)
```

**¿Por qué `verbose=0`?**
- No mostrar mensajes en consola durante la predicción

---

#### **PASO 5: Ajuste con Palabras Clave Negativas**

```python
palabras_texto = texto.lower().split()
palabras_negativas_fuertes = ["pésimo", "pésima", "horrible", "terrible", 
                               "fatal", "malo", "mala", "malos", "malas"]

tiene_negacion_fuerte = any(palabra in palabras_negativas_fuertes 
                            for palabra in palabras_texto)
```

**¿Qué hace `any()`?**
Retorna `True` si **al menos una** palabra está en la lista.

**Equivalente con bucle:**
```python
tiene_negacion_fuerte = False
for palabra in palabras_texto:
    if palabra in palabras_negativas_fuertes:
        tiene_negacion_fuerte = True
        break
```

---

```python
if tiene_negacion_fuerte and probabilidad < 0.65:
    etiqueta = "negativo"
    probabilidad = max(0.3, probabilidad - 0.2)
elif probabilidad >= 0.5:
    etiqueta = "positivo"
else:
    etiqueta = "negativo"
```

**Lógica:**

**Caso 1:** Tiene palabra muy negativa Y probabilidad dudosa
```python
texto = "El servicio fue pésimo"
probabilidad = 0.55  # Cerca del umbral

# Ajuste:
etiqueta = "negativo"
probabilidad = 0.55 - 0.2 = 0.35
```

**Caso 2:** Probabilidad ≥ 0.5
```python
probabilidad = 0.8
etiqueta = "positivo"
```

**Caso 3:** Probabilidad < 0.5
```python
probabilidad = 0.3
etiqueta = "negativo"
```

**¿Por qué este ajuste?**
- Mejora la detección de comentarios muy negativos
- A veces el modelo no detecta bien palabras extremas
- Es una **heurística adicional** que complementa la red neuronal

---

#### **PASO 6: Retornar Resultado**

```python
return {
    "ok": True,
    "etiqueta": etiqueta,
    "confianza": float(probabilidad)
}
```

**Ejemplo de retorno:**
```python
{
    "ok": True,
    "etiqueta": "positivo",
    "confianza": 0.85
}
```

---

## 🎓 Decisiones de Diseño

### **Tabla Resumen**

| Decisión | Alternativa | ¿Por qué esto? |
|----------|-------------|----------------|
| **Red neuronal profunda (4 capas)** | Red simple (1-2 capas) | ✅ Mejor para captar patrones complejos<br>✅ Entiende contexto y negaciones |
| **TF-IDF en lugar de Word2Vec** | Word embeddings | ✅ Más simple de implementar<br>✅ Funciona bien con pocos datos |
| **N-grams (1,3)** | Solo palabras individuales | ✅ Captura frases ("muy bueno")<br>✅ Detecta negaciones ("no recomiendo") |
| **Dropout 40%** | Sin dropout o menos | ✅ Evita overfitting<br>✅ Dataset relativamente pequeño |
| **ReLU en capas ocultas** | Sigmoid o Tanh | ✅ Más rápida<br>✅ Evita vanishing gradient |
| **Sigmoid en salida** | Softmax | ✅ Clasificación binaria<br>✅ Output entre 0 y 1 |
| **Adam optimizer** | SGD | ✅ Aprende más rápido<br>✅ Auto-ajusta learning rate |
| **20 epochs** | 10 o 50 | ✅ Balance entre tiempo y precisión<br>✅ Evita overfitting |
| **Batch size 16** | 32 o 64 | ✅ Bueno para datasets pequeños<br>✅ Más actualizaciones de pesos |
| **Conservar negaciones** | Eliminar todas las stopwords | ✅ "no bueno" ≠ "bueno"<br>✅ Crítico para sentimientos |
| **Ajuste heurístico final** | Solo red neuronal | ✅ Mejora detección de extremos<br>✅ Compensa limitaciones del modelo |

---

### **Arquitectura: ¿Por qué esta estructura?**

```
Input (5000) → 256 → 128 → 64 → 32 → 1 (Output)
```

**Pirámide invertida:**
- **Inicio (256):** Capacidad para aprender muchos patrones
- **Medio (128, 64):** Combina patrones en representaciones abstractas
- **Final (32):** Representación compacta del sentimiento
- **Salida (1):** Decisión final (positivo/negativo)

**Alternativas descartadas:**
```
# Muy simple (poco poder de aprendizaje)
5000 → 64 → 1

# Muy compleja (overfitting con pocos datos)
5000 → 512 → 512 → 256 → 256 → 128 → 1
```

---

### **Complejidad Computacional**

#### **Entrenamiento:**
- **Tiempo:** ~2-5 minutos (depende del hardware)
- **Memoria:** ~500 MB RAM
- **Operaciones por epoch:** Millones de multiplicaciones matriciales

#### **Predicción:**
- **Tiempo:** <100 ms por comentario
- **Memoria:** ~200 MB RAM (modelo cargado)

---

## 🔄 Flujo Completo del Código

### **Diagrama de Flujo: Entrenamiento**

```
┌─────────────────────────────┐
│ entrenar_modelo(df)         │
└──────────┬──────────────────┘
           │
           ↓
┌─────────────────────────────┐
│ 1. Limpiar datos            │
│    - Eliminar vacíos        │
│    - Aplicar limpiar_texto()│
└──────────┬──────────────────┘
           │
           ↓
┌─────────────────────────────┐
│ 2. Vectorización TF-IDF     │
│    - fit_transform()        │
│    - Guardar vectorizador   │
└──────────┬──────────────────┘
           │
           ↓
┌─────────────────────────────┐
│ 3. Preparar etiquetas       │
│    - positivo → 1           │
│    - negativo → 0           │
└──────────┬──────────────────┘
           │
           ↓
┌─────────────────────────────┐
│ 4. Dividir datos            │
│    - 80% entrenamiento      │
│    - 20% prueba             │
└──────────┬──────────────────┘
           │
           ↓
┌─────────────────────────────┐
│ 5. Crear red neuronal       │
│    - 4 capas Dense          │
│    - Dropout                │
│    - Compilar               │
└──────────┬──────────────────┘
           │
           ↓
┌─────────────────────────────┐
│ 6. Entrenar (20 epochs)     │
│    - Ajustar pesos          │
│    - Validación             │
└──────────┬──────────────────┘
           │
           ↓
┌─────────────────────────────┐
│ 7. Guardar modelo           │
└──────────┬──────────────────┘
           │
           ↓
┌─────────────────────────────┐
│ 8. Evaluar y generar        │
│    gráficos                 │
└──────────┬──────────────────┘
           │
           ↓
┌─────────────────────────────┐
│ RETORNAR resultados         │
│ {accuracy, gráficos, ...}   │
└─────────────────────────────┘
```

---

### **Diagrama de Flujo: Predicción**

```
┌─────────────────────────────┐
│ predecir(texto)             │
└──────────┬──────────────────┘
           │
           ↓
┌─────────────────────────────┐
│ 1. Cargar modelo y          │
│    vectorizador             │
└──────────┬──────────────────┘
           │
       ┌───┴───┐
       │ ¿Existe? │
       └───┬───┘
           │
    ┌──────┴──────┐
   NO             SÍ
    │              │
    ↓              ↓
┌─────────┐  ┌─────────────────┐
│ ERROR   │  │ 2. Limpiar texto│
│ Retornar│  └────────┬─────────┘
└─────────┘           │
                      ↓
           ┌──────────────────────┐
           │ 3. Vectorizar        │
           │    (transform)       │
           └──────────┬───────────┘
                      │
                      ↓
           ┌──────────────────────┐
           │ 4. Predecir con      │
           │    modelo.predict()  │
           └──────────┬───────────┘
                      │
                      ↓
           ┌──────────────────────┐
           │ 5. Ajustar con       │
           │    heurística        │
           └──────────┬───────────┘
                      │
                      ↓
           ┌──────────────────────┐
           │ 6. RETORNAR          │
           │ {etiqueta, confianza}│
           └──────────────────────┘
```

---

## 🎤 Puntos Clave para Presentar

### **1. Preprocesamiento**
> "Antes de entrenar, limpiamos el texto: eliminamos símbolos, URLs y stopwords. **Pero conservamos negaciones** porque cambian completamente el sentimiento."

### **2. Vectorización**
> "Las redes neuronales no entienden palabras, solo números. Usamos **TF-IDF** para convertir cada comentario en un vector de 5000 números que representa la importancia de cada palabra."

### **3. Arquitectura**
> "Diseñamos una red neuronal **profunda con 4 capas ocultas** que aprende patrones cada vez más abstractos: desde palabras individuales hasta el sentimiento general del comentario."

### **4. Regularización**
> "Usamos **Dropout** para evitar que el modelo memorice. Apagamos aleatoriamente 40% de las neuronas durante el entrenamiento, forzándolo a aprender patrones generales que funcionen con comentarios nuevos."

### **5. Entrenamiento**
> "El modelo ve los datos **20 veces (epochs)**, aprendiendo más en cada pasada. Usamos 80% para entrenar y 20% para probar qué tan bien generaliza."

### **6. Predicción**
> "Para predecir un comentario nuevo, lo limpiamos, lo vectorizamos con el **mismo vocabulario** del entrenamiento, y la red neuronal nos da una probabilidad entre 0 y 1. Mayor a 0.5 es positivo, menor es negativo."

---

## ✅ Checklist para Entender el Código

- ✅ Entiendo qué son las stopwords y por qué se eliminan
- ✅ Sé qué es TF-IDF y cómo convierte texto en números
- ✅ Entiendo la arquitectura de la red neuronal (capas, neuronas)
- ✅ Sé qué hacen ReLU y Sigmoid
- ✅ Entiendo qué es Dropout y por qué se usa
- ✅ Sé cómo se divide en entrenamiento/validación/prueba
- ✅ Entiendo qué hace Adam optimizer
- ✅ Sé interpretar la matriz de confusión
- ✅ Entiendo el flujo completo: entrenar → guardar → cargar → predecir

---

**Autor**: Sistema de Salud - Módulo de Análisis de Sentimientos  
**Documento**: Explicación Técnica de la Implementación  
**Fecha**: Noviembre 2025  
**Versión**: 1.0
