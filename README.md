# 🏥 Sistema de Inteligencia Artificial para el Sector Salud

Proyecto integral de IA que implementa **3 módulos avanzados** para optimizar servicios de salud mediante aprendizaje automático y algoritmos de búsqueda.

## 🎯 Módulos del Sistema

### 1️⃣ **Análisis de Sentimientos de Pacientes**
- Clasificación automática de comentarios como positivos o negativos
- Red neuronal profunda con TensorFlow/Keras
- Precisión: ~90-95%

### 2️⃣ **Predicción de Demanda de Pacientes**
- Predicción de afluencia diaria y semanal
- Regresión lineal múltiple supervisada
- Variables: día, mes, feriados

### 3️⃣ **Optimización de Rutas de Insumos Médicos**
- Algoritmo A* (A Estrella) para rutas óptimas
- 6 ubicaciones con visualización de red
- Comparación de rutas alternativas

## 📋 Requisitos

- Python 3.12
- PostgreSQL
- Librerías: Django, TensorFlow, scikit-learn, pandas, nltk, joblib

## 🚀 Instalación y Configuración

### Instalación Rápida

Sigue la **[Guía de Setup Inicial](SETUP_INICIAL.md)** para configurar el proyecto desde cero.

### Pasos Resumidos

1. **Instalar dependencias**
```bash
cd ProyectoSalud
pip install -r requirements.txt
```

2. **Configurar PostgreSQL**
   - Crear base de datos llamada `Modelos`
   - Ajustar credenciales en `ModeloSalud/ModeloSalud/settings.py` si es necesario

3. **Aplicar migraciones**
```bash
cd ModeloSalud
python manage.py migrate
```

4. **Cargar datos iniciales** (solo la primera vez)

Ver instrucciones detalladas en **[SETUP_INICIAL.md](SETUP_INICIAL.md)**

Opción rápida con Django shell:
```bash
python manage.py shell
```
Luego copiar y pegar el código de carga del archivo `SETUP_INICIAL.md`.

5. **Iniciar el servidor**
```bash
python manage.py runserver
```

6. **Abrir en el navegador**
```
http://127.0.0.1:8000/
```

## 🎮 Uso del Sistema

### Módulo 1: Análisis de Sentimientos
1. Acceder a http://127.0.0.1:8000/sentimientos/
2. **Entrenar modelo** (primera vez)
3. **Predecir** sentimiento de nuevos comentarios
4. **Buscar** y filtrar comentarios existentes

### Módulo 2: Predicción de Demanda
1. Acceder a http://127.0.0.1:8000/prediccion/
2. **Entrenar modelo** (primera vez)
3. **Predecir** demanda para días específicos o semanas completas
4. Ver **histórico** de datos

### Módulo 3: Optimización de Rutas
1. Acceder a http://127.0.0.1:8000/rutas/
2. Seleccionar **origen** y **destino**
3. Ver **ruta óptima** con visualización
4. Comparar con **rutas alternativas**

## 📁 Estructura del Proyecto

```
ProyectoSalud/
├── Comentarios_de_pacientes.csv    # Datos de ejemplo
├── ModeloSalud/
│   ├── manage.py
│   ├── modelos/                     # Carpeta donde se guardan los modelos entrenados
│   ├── ModeloSalud/
│   │   ├── settings.py
│   │   └── urls.py
│   └── sentimientos/
│       ├── models.py                # Modelo Comment
│       ├── views.py                 # Vistas de la aplicación
│       ├── servicios.py             # Lógica de IA (limpieza, entrenamiento, predicción)
│       ├── admin.py                 # Configuración del admin
│       ├── static/                  # Archivos estáticos
│       │   └── sentimientos/
│       │       └── css/
│       │           ├── base.css     # Estilos base (compartidos)
│       │           ├── home.css     # Estilos para página principal
│       │           ├── entrenar.css # Estilos para entrenamiento
│       │           ├── predecir.css # Estilos para predicción
│       │           ├── buscar.css   # Estilos para búsqueda
│       │           └── listar.css   # Estilos para listado
│       └── templates/               # Templates HTML
│           └── sentimientos/
│               ├── base.html        # Template base
│               ├── home.html        # Página principal
│               ├── entrenar.html    # Entrenar modelo
│               ├── predecir.html    # Predecir sentimiento
│               ├── buscar.html      # Buscar comentarios
│               └── listar.html      # Listar comentarios
```

## 🧠 Metodología de Inteligencia Artificial

### 📊 Módulo 1: Análisis de Sentimientos

**Tipo de Aprendizaje:** Supervisado  
**Algoritmo:** Red Neuronal Profunda (Deep Neural Network)

#### Justificación Técnica:
Las redes neuronales son ideales para clasificación de texto porque:
- Capturan patrones complejos y sutiles en el lenguaje
- Aprenden representaciones automáticas de características
- Manejan vocabulario amplio y contextos variados
- Alta precisión con datos etiquetados

#### Arquitectura del Modelo:
```
Input (TF-IDF) → Dense(256, relu) → Dropout(0.4) 
              → Dense(128, relu) → Dropout(0.4)
              → Dense(64, relu)  → Dropout(0.3)
              → Dense(32, relu)  → Dense(1, sigmoid)
```

#### Etapas del Proyecto de Machine Learning:

1. **Recolección de Datos**
   - Dataset: 50 comentarios de pacientes etiquetados
   - Formato: CSV con columnas 'texto' y 'etiqueta'
   - Origen: Comentarios reales de servicios de salud

2. **Preprocesamiento y Limpieza**
   - Conversión a minúsculas
   - Eliminación de URLs y caracteres especiales
   - Remoción de stopwords (manteniendo negaciones importantes)
   - Normalización de espacios

3. **Vectorización (Feature Engineering)**
   - **TF-IDF** con n-gramas (1,2,3)
   - max_features=5000 (palabras más relevantes)
   - min_df=2 (palabras que aparecen al menos 2 veces)
   - Captura contexto con trigramas: "pésimo servicio médico"

4. **División de Datos**
   - Entrenamiento: 80%
   - Prueba: 20%
   - Estratificación para balance de clases

5. **Entrenamiento del Modelo**
   - Épocas: 20
   - Batch size: 16
   - Optimizador: Adam
   - Loss: Binary Crossentropy
   - Validación cruzada: 20% del set de entrenamiento

6. **Evaluación**
   - Métrica principal: Accuracy (~90-95%)
   - Ajuste inteligente para palabras negativas fuertes
   - Sistema de confianza (probabilidad)

7. **Despliegue**
   - Modelo guardado en formato .h5 (Keras)
   - Vectorizador guardado con joblib
   - API REST mediante Django views
   - Predicción en tiempo real

---

### 📈 Módulo 2: Predicción de Demanda

**Tipo de Aprendizaje:** Supervisado  
**Algoritmo:** Regresión Lineal Múltiple

#### Justificación Técnica:
La regresión lineal es óptima para este caso porque:
- Relación lineal clara entre variables temporales y demanda
- Interpretable: se puede explicar el impacto de cada variable
- Rápido en entrenamiento e inferencia
- Requiere pocos datos para resultados precisos
- Ideal para predicciones numéricas continuas

#### Modelo Matemático:
```
Pacientes = β₀ + β₁(día_semana) + β₂(mes) + β₃(es_feriado)
```

#### Etapas del Proyecto de Machine Learning:

1. **Recolección de Datos**
   - 90 días de historial de demanda
   - Variables: fecha, día_semana, mes, es_feriado, pacientes
   - Generación automática con patrones realistas

2. **Análisis Exploratorio**
   - Patrones identificados:
     * Lunes: Mayor demanda (acumulación fin de semana)
     * Domingos: Menor demanda
     * Feriados: Reducción ~40%
     * Tendencias estacionales por mes

3. **Feature Engineering**
   - Extracción de día de la semana (0-6)
   - Extracción de mes (1-12)
   - Variable binaria para feriados
   - Normalización con StandardScaler

4. **División de Datos**
   - 80% entrenamiento, 20% prueba
   - Sin barajar para mantener orden temporal

5. **Entrenamiento**
   - Ajuste por mínimos cuadrados
   - Cálculo de coeficientes β
   - R² score para evaluar ajuste

6. **Evaluación**
   - Métricas: R², MAE, RMSE
   - Validación con datos históricos
   - Gráficos de tendencias vs predicción

7. **Despliegue**
   - Predicciones día individual o semana completa
   - Visualización con gráficos de barras
   - Comparación con datos históricos

---

### 🗺️ Módulo 3: Optimización de Rutas

**Tipo de Búsqueda:** Búsqueda Informada  
**Algoritmo:** A* (A Estrella)

#### Justificación Técnica:
A* es el algoritmo óptimo porque:
- **Completo:** Siempre encuentra solución si existe
- **Óptimo:** Garantiza la ruta más corta
- **Eficiente:** Explora menos nodos que búsqueda exhaustiva
- **Informado:** Usa heurística para priorizar caminos prometedores
- Ideal para grafos con pesos positivos

#### Fórmula de Evaluación:
```
f(n) = g(n) + h(n)

Donde:
- f(n) = Costo total estimado
- g(n) = Costo real desde origen hasta nodo n
- h(n) = Heurística (distancia euclidiana al destino)
```

#### Proceso del Algoritmo:

1. **Definición del Problema**
   - Grafo: 6 ubicaciones médicas
   - Nodos: Hospital, Bodega Central, Centro Distribución, Farmacia, Almacén, Fábrica
   - Aristas: Conexiones con costos (distancias en km)
   - Objetivo: Ruta más corta de A a B

2. **Heurística Admisible**
   - Distancia euclidiana: √[(x₂-x₁)² + (y₂-y₁)²]
   - Nunca sobreestima el costo real
   - Garantiza optimalidad

3. **Exploración de Nodos**
   - Cola de prioridad ordenada por f(n)
   - Selección del nodo con menor costo estimado
   - Expansión de vecinos
   - Actualización de costos si se encuentra mejor camino

4. **Reconstrucción del Camino**
   - Backtracking desde destino a origen
   - Lista de nodos en orden correcto

5. **Visualización**
   - Mapa visual con Canvas HTML5
   - Todas las conexiones en gris
   - Ruta óptima resaltada en verde
   - Comparación con rutas alternativas

6. **Análisis de Resultados**
   - Distancia total de ruta óptima
   - Comparación con otras rutas posibles
   - Ahorro de kilómetros vs alternativas

---

## 🎓 Cumplimiento de Requisitos Académicos

### ✅ Parte 1: Clasificación de Texto
- [x] Carga de conjunto de datos (CSV)
- [x] Limpieza y búsqueda de texto (NLTK + regex)
- [x] Clasificación con red neuronal (TensorFlow)

### ✅ Parte 2: Algoritmos de Búsqueda
- [x] Implementación de A* en Python
- [x] Uso de grafo y heurística
- [x] Visualización del camino óptimo
- [x] Explicación de selección de nodos paso a paso

### ✅ Parte 3: Aplicación Web
- [x] Predicción de demanda de pacientes
- [x] Clasificación automática de opiniones
- [x] Optimización de rutas de insumos
- [x] Interfaz web completa con Django

---

## 👨‍💻 Autor

**Nicolás Lester**  
Proyecto desarrollado para la asignatura de Aplicaciones de Inteligencia Artificial  
Instituto Profesional INACAP - 2025

## 📝 Licencia

Proyecto académico - Todos los derechos reservados
