# 🔄 Carga Automática de Datos

## ¿Cómo funciona ahora?

Los archivos CSV se cargan **automáticamente** la primera vez que inicias el servidor Django, **sin necesidad de ejecutar comandos manuales**.

---

## 📋 Funcionamiento

### **Primera vez que ejecutas `python manage.py runserver`:**

```
Iniciando Django...
============================================================
🔄 Primera ejecución detectada - Sentimientos
   Cargando comentarios iniciales desde CSV...
============================================================

📂 Cargando comentarios desde: C:\Users\nicol\Desktop\ProyectoSalud\Comentarios_de_pacientes.csv
✅ Proceso completado!
   - Comentarios nuevos cargados: 74
   - Total en base de datos: 74

============================================================
✅ Comentarios cargados correctamente
============================================================

============================================================
🔄 Primera ejecución detectada - Predicción
   Cargando datos de demanda iniciales desde CSV...
============================================================

📂 Cargando datos desde: C:\Users\nicol\Desktop\ProyectoSalud\Datos_Demanda_Pacientes.csv
✅ Proceso completado!
  - Registros cargados: 90
  - Total en base de datos: 90

============================================================
✅ Datos de demanda cargados correctamente
============================================================

Servidor iniciado en http://127.0.0.1:8000/
```

### **Segunda vez en adelante:**

Los datos ya están en la base de datos, así que **no se vuelven a cargar**. El servidor inicia normalmente sin mensajes de carga.

---

## 🎯 Ventajas

✅ **No necesitas ejecutar comandos manuales**  
✅ **No se duplican datos** (solo carga si la tabla está vacía)  
✅ **Funciona automáticamente** al iniciar Django  
✅ **Rutas por defecto** (busca los CSV en la raíz del proyecto)

---

## 🛠️ Comandos manuales (opcionales)

Si necesitas recargar o forzar la carga, todavía puedes usar los comandos:

### Cargar comentarios manualmente:
```bash
# Usar ruta por defecto
python manage.py load_comments

# Especificar ruta personalizada
python manage.py load_comments --path="ruta/personalizada/comentarios.csv"

# Forzar carga aunque ya existan datos
python manage.py load_comments --force
```

### Cargar datos de demanda manualmente:
```bash
# Usar ruta por defecto
python manage.py load_demanda

# Especificar ruta personalizada
python manage.py load_demanda --path="ruta/personalizada/demanda.csv"

# Forzar recarga (BORRA datos existentes)
python manage.py load_demanda --force
```

---

## 📂 Ubicación esperada de los CSV

Por defecto, el sistema busca los archivos en:

```
ProyectoSalud/
├── Comentarios_de_pacientes.csv  ← Aquí
├── Datos_Demanda_Pacientes.csv   ← Aquí
└── ModeloSalud/
    └── manage.py
```

Si tus CSV están en otro lugar, usa el parámetro `--path` en los comandos manuales.

---

## ⚠️ Importante

- **Primera ejecución**: Los datos se cargan automáticamente
- **Ejecuciones siguientes**: Los datos YA están en PostgreSQL, no se recargan
- **Para resetear**: Usa `--force` en los comandos o elimina los registros desde la interfaz web

---

## 🔍 ¿Qué cambió?

### Antes:
```bash
# Tenías que ejecutar manualmente:
python manage.py load_comments --path="C:\Users\nicol\Desktop\ProyectoSalud\Comentarios_de_pacientes.csv"
python manage.py load_demanda --path="C:\Users\nicol\Desktop\ProyectoSalud\Datos_Demanda_Pacientes.csv"
```

### Ahora:
```bash
# Solo ejecutas:
python manage.py runserver

# Y todo se carga automáticamente si es necesario 🎉
```

---

## 🐛 Solución de problemas

### "No se encontró el archivo CSV"
- Verifica que los CSV estén en la raíz del proyecto
- O usa `--path` para especificar la ubicación exacta

### "Ya existen datos"
- Es normal, significa que los datos ya se cargaron anteriormente
- Si quieres recargar, usa `--force`

### Los datos no se cargan automáticamente
- Asegúrate de que las tablas estén vacías
- Ejecuta `python manage.py migrate` antes del primer `runserver`
