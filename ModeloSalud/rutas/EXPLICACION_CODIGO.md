# 💻 Explicación de la Implementación del Código A*

## 📋 Índice
1. [Introducción](#introducción)
2. [Estructura de Datos: El Grafo](#estructura-de-datos-el-grafo)
3. [Función Heurística](#función-heurística)
4. [Algoritmo A* - Implementación](#algoritmo-a---implementación)
5. [Funciones Auxiliares](#funciones-auxiliares)
6. [Decisiones de Diseño](#decisiones-de-diseño)
7. [Flujo Completo del Código](#flujo-completo-del-código)

---

## 🎯 Introducción

Este documento explica **CÓMO está implementado** el código del algoritmo A* en Python. No es la teoría del algoritmo, sino **qué hace cada parte del código y por qué está diseñado así**.

**Archivo:** `algoritmo_busqueda.py`

---

## 📊 Estructura de Datos: El Grafo

### 1️⃣ **Representación de Ubicaciones (Nodos)**

```python
UBICACIONES = {
    'Hospital': {'x': 0, 'y': 0},
    'Bodega Central': {'x': 5, 'y': 3},
    'Centro Distribucion': {'x': 3, 'y': 5},
    'Farmacia Principal': {'x': 7, 'y': 2},
    'Almacen Regional': {'x': 10, 'y': 6},
    'Fabrica Insumos': {'x': 12, 'y': 8},
}
```

#### **¿Cómo funciona?**
- **Tipo de dato:** Diccionario de diccionarios
- **Estructura:** `{nombre: {coordenadas}}`
- **Acceso:** `UBICACIONES['Hospital']['x']` → `0`

#### **¿Por qué un diccionario?**
✅ **Acceso rápido:** O(1) para obtener coordenadas  
✅ **Extensible:** Agregar nuevas ubicaciones sin cambiar código  
✅ **Legible:** Los nombres son las claves (auto-documentado)  
✅ **Flexible:** Cada ubicación puede tener propiedades adicionales  

#### **¿Para qué sirven las coordenadas?**
- Calcular la **heurística** (distancia en línea recta)
- Visualizar el grafo en un plano 2D
- Verificar posiciones relativas entre ubicaciones

**Ejemplo de uso:**
```python
# Obtener coordenadas del Hospital
x = UBICACIONES['Hospital']['x']  # 0
y = UBICACIONES['Hospital']['y']  # 0

# Iterar sobre todas las ubicaciones
for nombre, coords in UBICACIONES.items():
    print(f"{nombre}: ({coords['x']}, {coords['y']})")
```

---

### 2️⃣ **Representación de Conexiones (Aristas)**

```python
CONEXIONES = {
    'Hospital': [
        {'destino': 'Bodega Central', 'costo': 6},
        {'destino': 'Centro Distribucion', 'costo': 7},
    ],
    'Bodega Central': [
        {'destino': 'Hospital', 'costo': 6},
        {'destino': 'Farmacia Principal', 'costo': 4},
        {'destino': 'Centro Distribucion', 'costo': 3},
    ],
    # ... más conexiones
}
```

#### **¿Cómo funciona?**
- **Tipo de dato:** Diccionario de listas de diccionarios
- **Estructura:** `{origen: [{destino, costo}, {destino, costo}, ...]}`
- **Acceso:** `CONEXIONES['Hospital'][0]['destino']` → `'Bodega Central'`

#### **¿Por qué esta estructura? (Lista de Adyacencia)**
✅ **Eficiente:** Solo guardamos conexiones existentes  
✅ **Iterable:** Fácil recorrer vecinos con `for`  
✅ **Flexible:** Cada conexión guarda su propio costo  
✅ **Dirigido:** Podemos tener aristas unidireccionales  

#### **¿Qué representa el costo?**
- **Distancia real** en kilómetros
- **Tiempo** de viaje en minutos
- Cualquier métrica que queramos optimizar

**Ejemplo de uso:**
```python
# Obtener vecinos del Hospital
vecinos = CONEXIONES['Hospital']

# Iterar sobre cada vecino
for conexion in vecinos:
    destino = conexion['destino']
    costo = conexion['costo']
    print(f"Hospital → {destino}: {costo} km")

# Salida:
# Hospital → Bodega Central: 6 km
# Hospital → Centro Distribucion: 7 km
```

---

## 🧮 Función Heurística

```python
def calcular_heuristica(origen, destino):
    """
    Calcula la distancia en línea recta entre dos ubicaciones
    Utiliza la fórmula de distancia euclidiana
    """
    # Extraer coordenadas del origen
    x1, y1 = UBICACIONES[origen]['x'], UBICACIONES[origen]['y']
    
    # Extraer coordenadas del destino
    x2, y2 = UBICACIONES[destino]['x'], UBICACIONES[destino]['y']
    
    # Aplicar fórmula: d = √[(x2-x1)² + (y2-y1)²]
    distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    return distancia
```

### **Desglose Línea por Línea:**

#### **Línea 1-2: Extraer coordenadas del origen**
```python
x1, y1 = UBICACIONES[origen]['x'], UBICACIONES[origen]['y']
```
- **Desempaquetado de tupla:** Asigna `x1` e `y1` en una sola línea
- **Alternativa menos elegante:**
  ```python
  x1 = UBICACIONES[origen]['x']
  y1 = UBICACIONES[origen]['y']
  ```

#### **Línea 3-4: Extraer coordenadas del destino**
```python
x2, y2 = UBICACIONES[destino]['x'], UBICACIONES[destino]['y']
```
- Mismo proceso para el punto de destino

#### **Línea 5: Calcular distancia euclidiana**
```python
distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
```

**¿Qué hace cada parte?**
- `(x2 - x1)` → Diferencia en el eje X
- `**2` → Elevar al cuadrado
- `(y2 - y1)**2` → Diferencia en Y al cuadrado
- `+` → Sumar ambos cuadrados
- `math.sqrt()` → Raíz cuadrada del resultado

**Ejemplo numérico:**
```python
# Hospital (0,0) → Bodega (5,3)
x1, y1 = 0, 0
x2, y2 = 5, 3

distancia = math.sqrt((5-0)**2 + (3-0)**2)
         = math.sqrt(25 + 9)
         = math.sqrt(34)
         ≈ 5.83
```

### **¿Por qué separar esto en una función?**

✅ **Reutilización:** Se llama múltiples veces durante el algoritmo  
✅ **Mantenibilidad:** Si cambiamos la heurística, solo modificamos aquí  
✅ **Legibilidad:** `calcular_heuristica(a, b)` es más claro que la fórmula  
✅ **Testing:** Podemos probar la heurística independientemente  

### **¿Por qué usar `math.sqrt()`?**
- Es una función nativa de Python optimizada en C
- Más rápida que implementar nuestra propia raíz cuadrada
- Maneja casos especiales (números negativos, cero, etc.)

---

## 🎯 Algoritmo A* - Implementación

### **Firma de la Función**

```python
def buscar_ruta_optima(inicio, objetivo):
    """
    Implementación del algoritmo A* (A-Star / A-Estrella)
    Encuentra el camino más corto entre dos ubicaciones
    """
```

**Parámetros:**
- `inicio` (str): Nombre de la ubicación de partida
- `objetivo` (str): Nombre de la ubicación de destino

**Retorna:**
- `dict`: Diccionario con resultados (éxito, camino, costo, pasos)

---

### **PARTE 1: Inicialización de Estructuras de Datos**

```python
# Lista para registrar cada paso (debugging/visualización)
pasos = []

# Cola de prioridad (heap) para nodos a explorar
cola_prioridad = []
heapq.heappush(cola_prioridad, (0, inicio))

# Diccionario para rastrear de dónde venimos (reconstruir camino)
origen_nodo = {}
origen_nodo[inicio] = None

# Diccionario para guardar g(n) - costo real desde el inicio
costo_acumulado = {}
costo_acumulado[inicio] = 0

# Contador de pasos
paso_numero = 1
```

#### **Estructura 1: `pasos` (Lista)**
```python
pasos = []
```
- **Propósito:** Registrar la ejecución paso a paso
- **Tipo:** Lista de diccionarios
- **Uso:** Debugging y visualización en la interfaz web
- **Opcional:** No es necesaria para el algoritmo, solo para mostrar el proceso

#### **Estructura 2: `cola_prioridad` (Heap)**
```python
cola_prioridad = []
heapq.heappush(cola_prioridad, (0, inicio))
```

**¿Qué es?**
- Lista que usaremos como **min-heap** (montículo mínimo)
- Guardamos tuplas: `(prioridad, nodo)`
- La prioridad es `f(n) = g(n) + h(n)`

**¿Cómo funciona heapq?**
```python
import heapq

cola = []
heapq.heappush(cola, (14.6, 'Bodega'))    # Agregar
heapq.heappush(cola, (16.5, 'Centro'))    # Agregar
heapq.heappush(cola, (10.2, 'Farmacia'))  # Agregar

# El heap automáticamente mantiene el menor en [0]
print(cola)  # [(10.2, 'Farmacia'), (16.5, 'Centro'), (14.6, 'Bodega')]

# Extraer el menor
menor = heapq.heappop(cola)  # (10.2, 'Farmacia')
```

**¿Por qué heapq?**
- ✅ **Eficiente:** Inserción O(log n), extracción O(log n)
- ✅ **Automático:** Mantiene el orden sin intervención manual
- ✅ **Nativo:** No necesita librerías externas

**¿Por qué tuplas `(prioridad, nodo)`?**
- Python compara tuplas elemento por elemento
- `(10, 'A') < (15, 'B')` → Compara primero el 10 vs 15
- Si las prioridades son iguales, compara los nombres

**Inicialización:**
```python
heapq.heappush(cola_prioridad, (0, inicio))
```
- Agregamos el nodo inicial con prioridad 0
- `f(Hospital) = 0 + h(Hospital)` → En el inicio, g(n) = 0

#### **Estructura 3: `origen_nodo` (Diccionario)**
```python
origen_nodo = {}
origen_nodo[inicio] = None
```

**¿Qué guarda?**
- **Clave:** Nombre del nodo
- **Valor:** Nombre del nodo del que venimos

**Ejemplo durante la ejecución:**
```python
origen_nodo = {
    'Hospital': None,
    'Bodega': 'Hospital',
    'Farmacia': 'Bodega',
    'Almacen': 'Farmacia',
}
```

**¿Para qué sirve?**
- **Reconstruir el camino** al final
- Seguir la cadena desde el objetivo hasta el inicio

**¿Por qué `None` para el inicio?**
- El nodo inicial no viene de ningún lado
- `None` marca el final de la cadena al reconstruir

#### **Estructura 4: `costo_acumulado` (Diccionario)**
```python
costo_acumulado = {}
costo_acumulado[inicio] = 0
```

**¿Qué guarda?**
- **Clave:** Nombre del nodo
- **Valor:** g(n) - costo real desde el inicio

**Ejemplo durante la ejecución:**
```python
costo_acumulado = {
    'Hospital': 0,
    'Bodega': 6,
    'Farmacia': 10,
    'Almacen': 15,
}
```

**¿Para qué sirve?**
1. Calcular `f(n) = g(n) + h(n)`
2. Detectar si encontramos un camino más corto a un nodo
3. Obtener el costo total del camino final

---

### **PARTE 2: Bucle Principal**

```python
while cola_prioridad:
    # Extraer el nodo con menor f(n)
    _, nodo_actual = heapq.heappop(cola_prioridad)
```

#### **¿Qué hace `while cola_prioridad`?**
- Continúa mientras haya nodos por explorar
- Si la cola se vacía, no hay camino al objetivo
- Equivalente a: `while len(cola_prioridad) > 0`

#### **¿Qué hace `heapq.heappop()`?**
```python
_, nodo_actual = heapq.heappop(cola_prioridad)
```

**Desglose:**
- `heappop()` → Extrae y devuelve el elemento con menor prioridad
- Devuelve una tupla: `(prioridad, nodo)`
- `_` → Ignoramos la prioridad (no la necesitamos aquí)
- `nodo_actual` → Guardamos solo el nombre del nodo

**Ejemplo:**
```python
cola = [(14.6, 'Bodega'), (16.5, 'Centro')]
_, nodo = heapq.heappop(cola)
# _ = 14.6 (ignorado)
# nodo = 'Bodega' (usado)
```

**¿Por qué usar `_`?**
- Convención de Python para variables que no usaremos
- Indica claramente al lector "esto lo ignoramos"
- Más limpio que `prioridad, nodo` y luego no usar `prioridad`

---

### **PARTE 3: Registro de Pasos (Opcional)**

```python
# Registrar este paso para visualización
pasos.append({
    'paso': paso_numero,
    'nodo_explorado': nodo_actual,
    'costo_acumulado': costo_acumulado[nodo_actual],
    'heuristica': calcular_heuristica(nodo_actual, objetivo),
})
paso_numero += 1
```

**¿Qué hace?**
- Crea un diccionario con información del paso actual
- Lo agrega a la lista `pasos`
- Incrementa el contador

**¿Para qué sirve?**
- ✅ Debugging: Ver cómo avanza el algoritmo
- ✅ Visualización: Mostrar el proceso en la web
- ✅ Educación: Explicar cómo funciona A*

**⚠️ Nota:** Esta parte no es necesaria para que A* funcione, es solo para tracking.

---

### **PARTE 4: Condición de Éxito**

```python
if nodo_actual == objetivo:
    # Reconstruir el camino
    camino = []
    while nodo_actual is not None:
        camino.append(nodo_actual)
        nodo_actual = origen_nodo[nodo_actual]
    camino.reverse()
    
    return {
        'exito': True,
        'camino': camino,
        'costo_total': costo_acumulado[objetivo],
        'pasos': pasos
    }
```

#### **Verificación del Objetivo**
```python
if nodo_actual == objetivo:
```
- Compara el nodo que acabamos de sacar con el objetivo
- Si coinciden, ¡llegamos! Hora de reconstruir el camino

#### **Reconstrucción del Camino**
```python
camino = []
while nodo_actual is not None:
    camino.append(nodo_actual)
    nodo_actual = origen_nodo[nodo_actual]
camino.reverse()
```

**¿Cómo funciona?**

**Paso a paso:**
```python
# Estado de origen_nodo:
origen_nodo = {
    'Hospital': None,
    'Bodega': 'Hospital',
    'Farmacia': 'Bodega',
    'Almacen': 'Farmacia',
    'Fabrica': 'Almacen'
}

# Empezamos en el objetivo
nodo_actual = 'Fabrica'
camino = []

# Iteración 1:
camino.append('Fabrica')  # ['Fabrica']
nodo_actual = origen_nodo['Fabrica']  # 'Almacen'

# Iteración 2:
camino.append('Almacen')  # ['Fabrica', 'Almacen']
nodo_actual = origen_nodo['Almacen']  # 'Farmacia'

# Iteración 3:
camino.append('Farmacia')  # ['Fabrica', 'Almacen', 'Farmacia']
nodo_actual = origen_nodo['Farmacia']  # 'Bodega'

# Iteración 4:
camino.append('Bodega')  # ['Fabrica', 'Almacen', 'Farmacia', 'Bodega']
nodo_actual = origen_nodo['Bodega']  # 'Hospital'

# Iteración 5:
camino.append('Hospital')  # ['Fabrica', 'Almacen', 'Farmacia', 'Bodega', 'Hospital']
nodo_actual = origen_nodo['Hospital']  # None

# while termina porque nodo_actual es None
```

**Después del while:**
```python
camino = ['Fabrica', 'Almacen', 'Farmacia', 'Bodega', 'Hospital']
```

**¿Por qué está al revés?**
- Empezamos en el objetivo y retrocedimos hasta el inicio
- El camino real va del inicio al objetivo

**Solución: `reverse()`**
```python
camino.reverse()
# Ahora: ['Hospital', 'Bodega', 'Farmacia', 'Almacen', 'Fabrica']
```

#### **Retorno del Resultado**
```python
return {
    'exito': True,
    'camino': camino,
    'costo_total': costo_acumulado[objetivo],
    'pasos': pasos
}
```

**¿Por qué un diccionario?**
- ✅ **Auto-documentado:** Las claves explican qué es cada valor
- ✅ **Extensible:** Podemos agregar más información sin romper código
- ✅ **Flexible:** El código que llama puede verificar `resultado['exito']`

**Alternativa (menos clara):**
```python
# ❌ Menos legible
return True, camino, costo_acumulado[objetivo], pasos

# El código que llama:
exito, camino, costo, pasos = buscar_ruta_optima(a, b)
# ¿Qué es cada valor? No está claro
```

**Con diccionario:**
```python
# ✅ Más legible
resultado = buscar_ruta_optima(a, b)
if resultado['exito']:
    print(f"Camino: {resultado['camino']}")
    print(f"Costo: {resultado['costo_total']} km")
```

---

### **PARTE 5: Exploración de Vecinos**

```python
if nodo_actual in CONEXIONES:
    for conexion in CONEXIONES[nodo_actual]:
        vecino = conexion['destino']
        nuevo_costo = costo_acumulado[nodo_actual] + conexion['costo']
```

#### **Verificación de Conexiones**
```python
if nodo_actual in CONEXIONES:
```

**¿Por qué esta verificación?**
- Algunos nodos pueden no tener vecinos (ejemplo: Fábrica)
- Evita `KeyError` si intentamos acceder a `CONEXIONES[nodo_sin_vecinos]`
- Más robusto que asumir que todos los nodos tienen conexiones

**Alternativa sin verificación (❌ peligrosa):**
```python
# ❌ Puede dar error
for conexion in CONEXIONES[nodo_actual]:
    # KeyError si nodo_actual no está en CONEXIONES
```

#### **Iteración sobre Vecinos**
```python
for conexion in CONEXIONES[nodo_actual]:
    vecino = conexion['destino']
    nuevo_costo = costo_acumulado[nodo_actual] + conexion['costo']
```

**¿Qué hace cada línea?**

**Línea 1:** Iterar sobre la lista de conexiones
```python
CONEXIONES['Hospital']  # [{'destino': 'Bodega', 'costo': 6}, {...}]
```

**Línea 2:** Extraer el nombre del vecino
```python
vecino = conexion['destino']  # 'Bodega Central'
```

**Línea 3:** Calcular g(n) del vecino
```python
nuevo_costo = costo_acumulado[nodo_actual] + conexion['costo']
#             g(n) del nodo actual        +  costo de la arista
```

**Ejemplo numérico:**
```python
nodo_actual = 'Hospital'
costo_acumulado['Hospital'] = 0

# Primera conexión:
conexion = {'destino': 'Bodega Central', 'costo': 6}
vecino = 'Bodega Central'
nuevo_costo = 0 + 6 = 6  # g(Bodega) = 6

# Segunda conexión:
conexion = {'destino': 'Centro Distribucion', 'costo': 7}
vecino = 'Centro Distribucion'
nuevo_costo = 0 + 7 = 7  # g(Centro Dist) = 7
```

---

### **PARTE 6: Actualización de Costos** (LA MÁS IMPORTANTE)

```python
if vecino not in costo_acumulado or nuevo_costo < costo_acumulado[vecino]:
    costo_acumulado[vecino] = nuevo_costo
    prioridad = nuevo_costo + calcular_heuristica(vecino, objetivo)
    heapq.heappush(cola_prioridad, (prioridad, vecino))
    origen_nodo[vecino] = nodo_actual
```

#### **Condición de Actualización**
```python
if vecino not in costo_acumulado or nuevo_costo < costo_acumulado[vecino]:
```

**Esta es la LÓGICA CLAVE de A***

**Desglose de la condición:**

**Parte A:** `vecino not in costo_acumulado`
- Es la **primera vez** que visitamos este vecino
- No tenemos ningún camino previo a él
- **Acción:** Guardarlo con el costo actual

**Parte B:** `nuevo_costo < costo_acumulado[vecino]`
- Ya visitamos este vecino antes
- Pero ahora encontramos un **camino más barato**
- **Acción:** Actualizar con el nuevo costo mejor

**Operador `or`:**
- Si **cualquiera** de las dos condiciones es verdadera, actualizamos
- Solo NO actualizamos si ya tenemos un camino mejor

**Ejemplos:**

**Ejemplo 1: Primera visita**
```python
costo_acumulado = {'Hospital': 0}
vecino = 'Bodega'
nuevo_costo = 6

# ¿'Bodega' está en costo_acumulado? NO
# Condición A es TRUE → ACTUALIZAR
costo_acumulado['Bodega'] = 6
```

**Ejemplo 2: Camino mejor**
```python
costo_acumulado = {'Hospital': 0, 'Centro Dist': 7}
vecino = 'Centro Dist'
nuevo_costo = 9

# ¿'Centro Dist' está en costo_acumulado? SÍ
# Condición A es FALSE
# ¿9 < 7? NO
# Condición B es FALSE
# FALSE or FALSE = FALSE → NO ACTUALIZAR
```

**Ejemplo 3: Camino peor (ignorar)**
```python
costo_acumulado = {'Hospital': 0, 'Bodega': 6}
vecino = 'Bodega'
nuevo_costo = 6.5

# ¿'Bodega' está en costo_acumulado? SÍ
# Condición A es FALSE
# ¿6.5 < 6? NO
# Condición B es FALSE
# FALSE or FALSE = FALSE → NO ACTUALIZAR (mantener 6)
```

#### **Actualizar g(n)**
```python
costo_acumulado[vecino] = nuevo_costo
```
- Guardar el costo real g(n) para este vecino
- Sobrescribe el valor anterior si existía

#### **Calcular f(n) y Agregar a la Cola**
```python
prioridad = nuevo_costo + calcular_heuristica(vecino, objetivo)
heapq.heappush(cola_prioridad, (prioridad, vecino))
```

**Línea 1: Calcular f(n)**
```python
prioridad = nuevo_costo + calcular_heuristica(vecino, objetivo)
#           g(n)        +  h(n)
#           ↓              ↓
#       costo real    distancia estimada
```

**Ejemplo:**
```python
vecino = 'Bodega'
nuevo_costo = 6  # g(n)
h_n = calcular_heuristica('Bodega', 'Fabrica')  # 8.6
prioridad = 6 + 8.6 = 14.6  # f(n)
```

**Línea 2: Agregar a la cola**
```python
heapq.heappush(cola_prioridad, (14.6, 'Bodega'))
```
- Inserta el vecino en la cola de prioridad
- El heap lo coloca en la posición correcta según su f(n)
- Nodos con menor f(n) se explorarán primero

#### **Actualizar Origen**
```python
origen_nodo[vecino] = nodo_actual
```

**¿Qué hace?**
- Registra que llegamos al vecino desde `nodo_actual`
- Necesario para reconstruir el camino al final

**¿Por qué está dentro del `if`?**
- Si encontramos un mejor camino, también cambiamos el origen
- Si NO actualizamos el costo, tampoco cambiamos el origen

**Ejemplo:**
```python
nodo_actual = 'Hospital'
vecino = 'Bodega'

origen_nodo['Bodega'] = 'Hospital'
# Significa: llegamos a Bodega desde Hospital
```

**Si luego encontramos mejor camino:**
```python
nodo_actual = 'Centro Dist'
vecino = 'Bodega'
nuevo_costo = 5  # Mejor que 6

# Actualizar:
costo_acumulado['Bodega'] = 5
origen_nodo['Bodega'] = 'Centro Dist'  # ← Cambiamos el origen
```

---

### **PARTE 7: Manejo de Fallo**

```python
# Si salimos del while sin llegar al objetivo
return {
    'exito': False,
    'error': 'No se encontró una ruta entre las ubicaciones',
    'pasos': pasos
}
```

#### **¿Cuándo se ejecuta esto?**
- Cuando el `while cola_prioridad` termina
- Significa que exploramos todos los nodos alcanzables
- Nunca llegamos al objetivo

#### **¿Por qué puede pasar?**
- El grafo está **desconectado**
- No hay camino del inicio al objetivo
- Ejemplo: Si eliminamos todas las aristas que salen del Hospital

**Ejemplo:**
```python
CONEXIONES = {
    'Hospital': [],  # ← Sin vecinos!
    'Bodega': [{'destino': 'Farmacia', 'costo': 4}],
    # ...
}

# Buscar ruta Hospital → Fabrica
resultado = buscar_ruta_optima('Hospital', 'Fabrica')
# → {'exito': False, 'error': '...', 'pasos': [...]}
```

#### **¿Por qué retornar un diccionario?**
- ✅ Consistente con el retorno de éxito
- ✅ Permite manejar errores sin excepciones
- ✅ El código que llama puede verificar `resultado['exito']`

**Uso:**
```python
resultado = buscar_ruta_optima(origen, destino)

if resultado['exito']:
    print(f"Camino: {resultado['camino']}")
else:
    print(f"Error: {resultado['error']}")
```

---

## 🛠️ Funciones Auxiliares

### **obtener_ubicaciones()**

```python
def obtener_ubicaciones():
    """
    Retorna la lista de todas las ubicaciones del grafo
    """
    return list(UBICACIONES.keys())
```

#### **¿Qué hace?**
1. `UBICACIONES.keys()` → Obtiene las claves del diccionario
2. `list()` → Convierte el objeto keys a lista
3. Retorna: `['Hospital', 'Bodega Central', ...]`

#### **¿Por qué `.keys()`?**
- Solo queremos los nombres, no las coordenadas
- `.keys()` devuelve solo las claves del diccionario

#### **¿Por qué `list()`?**
- `.keys()` devuelve un objeto `dict_keys`, no una lista
- `list()` lo convierte a una lista real
- Más fácil de usar en templates y formularios

**Ejemplo de uso:**
```python
# En views.py
ubicaciones = obtener_ubicaciones()
# ['Hospital', 'Bodega Central', 'Centro Distribucion', ...]

# En el template HTML
<select name="origen">
    {% for ubicacion in ubicaciones %}
        <option value="{{ ubicacion }}">{{ ubicacion }}</option>
    {% endfor %}
</select>
```

#### **¿Por qué una función separada?**
✅ **Abstracción:** El código que llama no necesita saber cómo está estructurado UBICACIONES  
✅ **Reutilización:** Múltiples partes pueden necesitar esta lista  
✅ **DRY:** No repetimos `list(UBICACIONES.keys())` en todo el código  
✅ **Mantenibilidad:** Si cambiamos UBICACIONES, solo ajustamos aquí  

---

## 🎓 Decisiones de Diseño

### **Tabla Resumen de Decisiones**

| Decisión | Alternativa | ¿Por qué elegimos esto? |
|----------|-------------|-------------------------|
| **Diccionario para UBICACIONES** | Lista de objetos | ✅ Acceso O(1) por nombre<br>✅ Auto-documentado |
| **Lista de adyacencia para CONEXIONES** | Matriz de adyacencia | ✅ Eficiente en memoria<br>✅ Solo guarda aristas existentes |
| **Tres diccionarios separados** | Un solo diccionario con todo | ✅ Propósito específico para cada uno<br>✅ Más legible |
| **heapq para cola de prioridad** | Ordenar lista manualmente | ✅ Eficiente O(log n)<br>✅ Nativo de Python |
| **Reconstrucción hacia atrás** | Guardar todos los caminos | ✅ Menos memoria<br>✅ Más simple |
| **Retornar diccionario** | Retornar múltiples valores | ✅ Auto-documentado<br>✅ Extensible |
| **Tuplas (prioridad, nodo)** | Objetos personalizados | ✅ Simple<br>✅ Compatible con heapq |
| **Función auxiliar obtener_ubicaciones()** | Acceso directo | ✅ Abstracción<br>✅ Reutilización |

---

### **Complejidad Computacional**

#### **Tiempo:**
- **heappush:** O(log n)
- **heappop:** O(log n)
- **Calcular heurística:** O(1)
- **Buscar en diccionario:** O(1)
- **Total:** O(b^d) donde b = factor de ramificación, d = profundidad

#### **Espacio:**
- **cola_prioridad:** O(b^d) - en el peor caso
- **costo_acumulado:** O(n) - un elemento por nodo
- **origen_nodo:** O(n) - un elemento por nodo
- **Total:** O(b^d)

---

### **Ventajas de esta Implementación**

1. ✅ **Legible:** Nombres descriptivos, comentarios claros
2. ✅ **Eficiente:** Uso de heapq y diccionarios
3. ✅ **Mantenible:** Funciones separadas, responsabilidad única
4. ✅ **Extensible:** Fácil agregar nuevas ubicaciones o funcionalidades
5. ✅ **Robusta:** Maneja errores (sin camino, nodos sin vecinos)
6. ✅ **Debuggeable:** Registro de pasos para análisis

---

### **Posibles Mejoras**

#### **1. Validación de Entrada**
```python
def buscar_ruta_optima(inicio, objetivo):
    # Validar que las ubicaciones existan
    if inicio not in UBICACIONES:
        return {'exito': False, 'error': f'Ubicación no encontrada: {inicio}'}
    if objetivo not in UBICACIONES:
        return {'exito': False, 'error': f'Ubicación no encontrada: {objetivo}'}
    
    # ... resto del código
```

#### **2. Optimización: Detección Temprana**
```python
# Si encontramos el objetivo, podríamos terminar antes
# en lugar de esperar a que sea el menor f(n)
if vecino == objetivo:
    # Reconstruir y retornar inmediatamente
    pass
```

#### **3. Heurística Configurable**
```python
def buscar_ruta_optima(inicio, objetivo, heuristica=calcular_heuristica):
    # Permitir usar diferentes heurísticas
    h = heuristica(vecino, objetivo)
```

#### **4. Evitar Duplicados en Cola**
```python
# Mantener un set de nodos en la cola
# para evitar agregar el mismo nodo múltiples veces
nodos_en_cola = set()
```

---

## 🔄 Flujo Completo del Código

### **Diagrama de Flujo**

```
┌─────────────────────────────────────┐
│ buscar_ruta_optima(inicio, objetivo)│
└──────────────┬──────────────────────┘
               │
               ↓
┌──────────────────────────────────────┐
│ 1. Inicializar estructuras de datos  │
│    - cola_prioridad = [(0, inicio)]  │
│    - origen_nodo = {inicio: None}    │
│    - costo_acumulado = {inicio: 0}   │
└──────────────┬───────────────────────┘
               │
               ↓
┌──────────────────────────────────────┐
│ 2. BUCLE: while cola_prioridad       │
└──────────────┬───────────────────────┘
               │
               ↓
┌──────────────────────────────────────┐
│ 3. Sacar nodo con menor f(n)         │
│    nodo_actual = heappop()           │
└──────────────┬───────────────────────┘
               │
               ↓
       ┌───────┴───────┐
       │ ¿Es objetivo? │
       └───────┬───────┘
               │
        ┌──────┴──────┐
       SÍ             NO
        │              │
        ↓              ↓
┌───────────────┐  ┌─────────────────────────┐
│ Reconstruir   │  │ Explorar vecinos        │
│ camino y      │  │ for vecino in vecinos:  │
│ RETORNAR      │  └────────┬────────────────┘
│ {'exito':True}│           │
└───────────────┘           ↓
                  ┌─────────────────────────┐
                  │ Calcular nuevo_costo    │
                  │ = g(actual) + costo_arista│
                  └────────┬────────────────┘
                           │
                           ↓
              ┌────────────────────────────┐
              │ ¿Primera visita O mejor    │
              │  camino?                   │
              └────────┬───────────────────┘
                       │
                ┌──────┴──────┐
               SÍ             NO
                │              │
                ↓              ↓
    ┌───────────────────┐  ┌─────────┐
    │ Actualizar:       │  │ Ignorar │
    │ - costo_acumulado │  └─────────┘
    │ - origen_nodo     │
    │ - Agregar a cola  │
    └───────┬───────────┘
            │
            └──────┐
                   │
                   ↓
        ┌──────────────────────┐
        │ Volver al inicio del │
        │ BUCLE                │
        └──────────────────────┘
                   │
                   ↓
        ┌──────────────────────┐
        │ Cola vacía sin llegar│
        │ al objetivo          │
        │ RETORNAR             │
        │ {'exito': False}     │
        └──────────────────────┘
```

---

### **Ejemplo de Ejecución Completa**

**Entrada:**
```python
resultado = buscar_ruta_optima('Hospital', 'Fabrica Insumos')
```

**Traza de ejecución:**

```
INICIALIZACIÓN:
cola_prioridad = [(0, 'Hospital')]
costo_acumulado = {'Hospital': 0}
origen_nodo = {'Hospital': None}

────────────────────────────────────────

ITERACIÓN 1:
Sacar: (0, 'Hospital')
¿Es objetivo? NO
Vecinos: Bodega(6), Centro Dist(7)

  Procesar Bodega:
  - g(n) = 0 + 6 = 6
  - h(n) = 8.6
  - f(n) = 14.6
  - Primera visita → AGREGAR

  Procesar Centro Dist:
  - g(n) = 0 + 7 = 7
  - h(n) = 9.5
  - f(n) = 16.5
  - Primera visita → AGREGAR

cola_prioridad = [(14.6, 'Bodega'), (16.5, 'Centro Dist')]

────────────────────────────────────────

ITERACIÓN 2:
Sacar: (14.6, 'Bodega')
¿Es objetivo? NO
Vecinos: Hospital(6), Farmacia(4), Centro Dist(3)

  Procesar Hospital:
  - Ya tiene costo mejor → IGNORAR

  Procesar Farmacia:
  - g(n) = 6 + 4 = 10
  - h(n) = 7.8
  - f(n) = 17.8
  - Primera visita → AGREGAR

  Procesar Centro Dist:
  - g(n) = 6 + 3 = 9
  - g(n) anterior = 7
  - 9 > 7 → IGNORAR

cola_prioridad = [(16.5, 'Centro Dist'), (17.8, 'Farmacia')]

────────────────────────────────────────

ITERACIÓN 3:
Sacar: (16.5, 'Centro Dist')
¿Es objetivo? NO
Vecinos: Hospital(7), Bodega(3), Almacen(8)

  Todos tienen costos peores → IGNORAR

────────────────────────────────────────

ITERACIÓN 4:
Sacar: (17.8, 'Farmacia')
¿Es objetivo? NO
Vecinos: Bodega(4), Almacen(5)

  Procesar Almacen:
  - g(n) = 10 + 5 = 15
  - h(n) = 2.8
  - f(n) = 17.8
  - Primera visita → AGREGAR

────────────────────────────────────────

ITERACIÓN 5:
Sacar: (17.8, 'Almacen')
¿Es objetivo? NO
Vecinos: Centro Dist(8), Farmacia(5), Fabrica(4)

  Procesar Fabrica:
  - g(n) = 15 + 4 = 19
  - h(n) = 0 (es el objetivo)
  - f(n) = 19
  - Primera visita → AGREGAR

────────────────────────────────────────

ITERACIÓN 6:
Sacar: (19, 'Fabrica')
¿Es objetivo? SÍ!!!

Reconstruir camino:
  origen_nodo = {
    'Hospital': None,
    'Bodega': 'Hospital',
    'Farmacia': 'Bodega',
    'Almacen': 'Farmacia',
    'Fabrica': 'Almacen'
  }

  Fabrica ← Almacen ← Farmacia ← Bodega ← Hospital ← None

  Invertir: Hospital → Bodega → Farmacia → Almacen → Fabrica

────────────────────────────────────────

RESULTADO:
{
  'exito': True,
  'camino': ['Hospital', 'Bodega Central', 'Farmacia Principal',
             'Almacen Regional', 'Fabrica Insumos'],
  'costo_total': 19,
  'pasos': [...]
}
```

---

## ✅ Checklist para Entender el Código

- ✅ Entiendo cómo se representa el grafo (UBICACIONES y CONEXIONES)
- ✅ Sé qué es heapq y cómo funciona
- ✅ Entiendo las tres estructuras principales (cola, origen_nodo, costo_acumulado)
- ✅ Sé cuándo se actualiza un nodo (primera visita O mejor camino)
- ✅ Entiendo cómo se reconstruye el camino
- ✅ Sé por qué retornamos un diccionario
- ✅ Puedo explicar cada línea de la función principal
- ✅ Entiendo el flujo completo del algoritmo

---

## 🎤 Puntos Clave para Presentar

1. **"Usamos diccionarios de Python para representar el grafo de forma eficiente"**

2. **"La cola de prioridad con heapq nos da automáticamente el nodo más prometedor"**

3. **"Mantenemos tres estructuras: una para explorar, una para costos, y una para reconstruir"**

4. **"Solo actualizamos un nodo si es la primera vez O si encontramos un camino mejor"**

5. **"Reconstruimos el camino hacia atrás siguiendo la cadena de padres"**

6. **"Retornamos un diccionario para tener resultados claros y extensibles"**

---

**Autor**: Sistema de Salud - Módulo de Optimización de Rutas  
**Documento**: Explicación Técnica de la Implementación  
**Fecha**: Noviembre 2025  
**Versión**: 1.0
