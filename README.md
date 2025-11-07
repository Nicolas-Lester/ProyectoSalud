# 🏥 Sistema de Análisis de Sentimientos de Pacientes

Proyecto de clasificación de texto usando redes neuronales para analizar comentarios de pacientes y clasificarlos como positivos o negativos.

## 🎯 Características

- **Clasificación de texto** usando redes neuronales (TensorFlow/Keras)
- **Limpieza de texto** con NLTK (eliminación de stopwords en español)
- **Vectorización TF-IDF** para convertir texto a números
- **Interfaz web interactiva** con Django
- **Búsqueda y filtrado** de comentarios
- **Predicción en tiempo real** de sentimientos

## 📋 Requisitos

- Python 3.12
- PostgreSQL
- Librerías: Django, TensorFlow, scikit-learn, pandas, nltk, joblib

## 🚀 Instalación

1. **Clonar el repositorio**
```bash
cd ProyectoSalud
```

2. **Instalar dependencias**
```bash
pip install django tensorflow scikit-learn pandas nltk joblib psycopg2
```

3. **Configurar la base de datos PostgreSQL**
   - Crear base de datos llamada `Modelos`
   - Ajustar credenciales en `ModeloSalud/settings.py` si es necesario

4. **Aplicar migraciones**
```bash
cd ModeloSalud
python manage.py makemigrations
python manage.py migrate
```

5. **Crear superusuario (opcional)**
```bash
python manage.py createsuperuser
```

## 📊 Cargar datos

Cargar comentarios desde el archivo CSV:

```bash
python manage.py load_comments --path ..\Comentarios_de_pacientes.csv
```

## 🎮 Uso

1. **Iniciar el servidor**
```bash
python manage.py runserver
```

2. **Abrir en el navegador**
```
http://localhost:8000
```

3. **Flujo de trabajo:**
   - Ver los comentarios cargados
   - Entrenar el modelo con los datos
   - Usar la función de predicción para clasificar nuevos comentarios
   - Buscar y filtrar comentarios por sentimiento

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
│       ├── templates/               # Templates HTML
│       │   └── sentimientos/
│       │       ├── base.html        # Template base
│       │       ├── home.html        # Página principal
│       │       ├── entrenar.html    # Entrenar modelo
│       │       ├── predecir.html    # Predecir sentimiento
│       │       ├── buscar.html      # Buscar comentarios
│       │       └── listar.html      # Listar comentarios
│       └── management/
│           └── commands/
│               └── load_comments.py # Comando para cargar CSV
```

## 🧠 Modelo de IA

- **Arquitectura:** Red neuronal secuencial
  - Capa Dense (128 neuronas, ReLU)
  - Dropout (0.3)
  - Capa Dense (64 neuronas, ReLU)
  - Capa Dense (1 neurona, Sigmoid)

- **Preprocesamiento:**
  - Limpieza de URLs
  - Eliminación de caracteres especiales
  - Eliminación de stopwords en español
  - Vectorización TF-IDF con bigramas

## 👨‍💻 Autor

Proyecto desarrollado para la asignatura de Aplicaciones de Inteligencia Artificial

## 📝 Licencia

Proyecto académico - 2025
