# 🚀 SETUP INICIAL - ProyectoSalud

Configuración del proyecto en **3 pasos simples**.

---

## 📋 Requisitos

- Python 3.12
- PostgreSQL con base de datos `Modelos` creada

---

## 🔧 Instalación

### 1. Instalar dependencias
```cmd
cd C:\Users\nicol\Desktop\ProyectoSalud
pip install -r requirements.txt
```

### 2. Crear tablas en PostgreSQL
```cmd
cd ModeloSalud
python manage.py migrate
```

### 3. Cargar datos desde CSV (solo una vez)
```cmd
python cargar_datos_iniciales.py
```

Este script carga automáticamente:
- ✅ 74 comentarios de pacientes
- ✅ 90+ registros de demanda

Los datos quedan guardados permanentemente en PostgreSQL.

---

## 🚀 Ejecutar el proyecto

```cmd
python manage.py runserver
```

Abre: **http://127.0.0.1:8000/**

---

## 🔄 Resetear datos (opcional)

Si necesitas borrar y volver a cargar:

```cmd
python manage.py shell
```

```python
from sentimientos.models import Comment
from prediccion.models import DemandaPacientes

Comment.objects.all().delete()
DemandaPacientes.objects.all().delete()
exit()
```

Luego ejecuta de nuevo: `python cargar_datos_iniciales.py`

---

## 📝 Notas

- Los CSV solo se usan **una vez** al inicio
- Después de la carga, todo funciona desde **PostgreSQL**
- Los modelos hacen la limpieza de datos automáticamente

---

**¡Listo!** 🎉
