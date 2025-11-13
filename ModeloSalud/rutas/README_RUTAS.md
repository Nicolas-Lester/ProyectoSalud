# 🗺️ Módulo de Optimización de Rutas con A* (A-Estrella)

## 📋 Índice
1. [Introducción](#introducción)
2. [¿Qué es el Algoritmo A*?](#qué-es-el-algoritmo-a)
3. [Librerías Utilizadas](#librerías-utilizadas)
4. [Estructura del Código](#estructura-del-código)
5. [Funcionamiento Detallado](#funcionamiento-detallado)
6. [Ejemplo Práctico Paso a Paso](#ejemplo-práctico-paso-a-paso)
7. [Casos de Uso](#casos-de-uso)

---

## 🎯 Introducción

Este módulo implementa el **Algoritmo A*** para encontrar la ruta más corta entre ubicaciones en una red de distribución de insumos médicos. El sistema optimiza el transporte entre:

- Hospital (punto de inicio)
- Bodega Central
- Centro de Distribución
- Farmacia Principal
- Almacén Regional
- Fábrica de Insumos (punto final típico)

---

## 🧠 ¿Qué es el Algoritmo A*?

### Definición
**A*** (A-Estrella) es un algoritmo de búsqueda informada que encuentra el camino más corto entre dos nodos en un grafo, usando una función de costo que combina:

```
f(n) = g(n) + h(n)

Donde:
- f(n) = Costo total estimado
- g(n) = Costo real desde el inicio hasta el nodo actual
- h(n) = Estimación (heurística) del costo del nodo actual al objetivo
```

### Historia
- **Creado en**: 1968
- **Autores**: Peter Hart, Nils Nilsson y Bertram Raphael
- **Lugar**: Stanford Research Institute (SRI)
- **Propósito original**: Navegación de robots

### ¿Por qué se llama A*?
- **A** = "Algorithm A" (Algoritmo A)
- ***** (asterisco) = Versión óptima y completa del algoritmo

### Ventajas
✅ **Óptimo**: Siempre encuentra la ruta más corta (si existe)  
✅ **Completo**: Si hay solución, la encuentra  
✅ **Eficiente**: Más rápido que Dijkstra gracias a la heurística  
✅ **Versátil**: Usado en GPS, videojuegos, robótica, logística  

---

## 📚 Librerías Utilizadas

### 1. **heapq** - Cola de Prioridad

```python
import heapq
```

#### ¿Qué es heapq?
Es un módulo nativo de Python que implementa una **cola de prioridad** usando una estructura de datos llamada **heap** (montículo).

#### ¿Qué es un Heap?
Un **heap** es un árbol binario especial donde:
- El padre siempre es menor que sus hijos (min-heap)
- Permite obtener el elemento más pequeño en **O(1)** (tiempo constante)
- Permite insertar elementos en **O(log n)** (tiempo logarítmico)

#### Visualización de un Heap:
```
        1
       / \
      3   2
     / \ / \
    5  4 8  7

Orden de extracción: 1, 2, 3, 4, 5, 7, 8
```

#### Funciones utilizadas en nuestro código:

##### **heapq.heappush(lista, elemento)**
```python
cola_prioridad = []
heapq.heappush(cola_prioridad, (5, 'Bodega'))
heapq.heappush(cola_prioridad, (2, 'Hospital'))
heapq.heappush(cola_prioridad, (8, 'Farmacia'))

# Internamente organiza: [(2, 'Hospital'), (5, 'Bodega'), (8, 'Farmacia')]
```
- **Propósito**: Inserta un elemento manteniendo el orden del heap
- **Complejidad**: O(log n)
- **En A***: Agrega nodos a explorar ordenados por f(n)

##### **heapq.heappop(lista)**
```python
elemento = heapq.heappop(cola_prioridad)
# Devuelve: (2, 'Hospital') - El de menor prioridad
```
- **Propósito**: Extrae y devuelve el elemento más pequeño
- **Complejidad**: O(log n)
- **En A***: Obtiene el nodo más prometedor para explorar

#### ¿Por qué usar heapq en A*?
A* necesita siempre explorar el nodo con **menor f(n)**. El heap garantiza que siempre obtengamos ese nodo eficientemente.

**Comparación de rendimiento:**
```python
# Con lista normal (búsqueda lineal):
min_elemento = min(lista)  # O(n) - Lento con muchos nodos
lista.remove(min_elemento)

# Con heapq (heap):
min_elemento = heapq.heappop(lista)  # O(log n) - Rápido
```

---

### 2. **math** - Funciones Matemáticas

```python
import math
```

#### ¿Qué es math?
Módulo nativo de Python con funciones matemáticas avanzadas.

#### Función utilizada: **math.sqrt()**

```python
distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
```

##### ¿Qué hace sqrt()?
Calcula la **raíz cuadrada** de un número.

```python
math.sqrt(9)   # = 3.0
math.sqrt(16)  # = 4.0
math.sqrt(25)  # = 5.0
```

##### ¿Por qué la usamos?
Para calcular la **distancia euclidiana** entre dos puntos en un plano 2D:

**Fórmula de distancia euclidiana:**
```
d = √[(x₂ - x₁)² + (y₂ - y₁)²]
```

**Ejemplo visual:**
```
Punto A (0, 0) → Hospital
Punto B (5, 3) → Bodega

Distancia = √[(5-0)² + (3-0)²]
         = √[25 + 9]
         = √34
         ≈ 5.83 unidades
```

Esta distancia es nuestra **heurística h(n)**: una estimación optimista de la distancia real.

---

## 🏗️ Estructura del Código

### Archivo: `algoritmo_busqueda.py`

```
📁 rutas/
  ├── algoritmo_busqueda.py  ← Lógica del algoritmo A*
  ├── views.py               ← Vistas de Django (interfaz web)
  ├── urls.py                ← Rutas URL
  ├── models.py              ← Modelos (vacío, no usa BD)
  └── templates/
      └── rutas/
          └── home.html      ← Interfaz HTML
```

---

## 🔍 Funcionamiento Detallado

### 1️⃣ **Definición del Grafo**

#### UBICACIONES (Nodos)
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

**¿Qué representa?**
- Cada ubicación es un **nodo** del grafo
- Las coordenadas (x, y) son posiciones en un plano imaginario
- Se usan para calcular la distancia en línea recta (heurística)

**Visualización del mapa:**
```
    Y
    8  |                        ● Fábrica (12,8)
    7  |
    6  |              ● Almacén (10,6)
    5  |      ● Centro Dist (3,5)
    4  |
    3  |          ● Bodega (5,3)
    2  |                  ● Farmacia (7,2)
    1  |
    0  | ● Hospital (0,0)
       |_________________________________ X
          0  1  2  3  4  5  6  7  8  9  10 11 12
```

#### CONEXIONES (Aristas)
```python
CONEXIONES = {
    'Hospital': [
        {'destino': 'Bodega Central', 'costo': 6},
        {'destino': 'Centro Distribucion', 'costo': 7},
    ],
    # ... más conexiones
}
```

**¿Qué representa?**
- Cada conexión es una **arista** (camino) entre dos nodos
- El **costo** es la distancia real en kilómetros o tiempo en minutos
- No todas las ubicaciones están conectadas directamente

**Ejemplo de grafo con conexiones:**
```
Hospital ----6---- Bodega Central ----4---- Farmacia
    |                    |                      |
    7                    3                      5
    |                    |                      |
Centro Dist --------8------- Almacén ----4---- Fábrica
```

---

### 2️⃣ **Función Heurística**

```python
def calcular_heuristica(origen, destino):
    """
    Calcula la distancia en línea recta entre dos ubicaciones
    """
    x1, y1 = UBICACIONES[origen]['x'], UBICACIONES[origen]['y']
    x2, y2 = UBICACIONES[destino]['x'], UBICACIONES[destino]['y']
    
    distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distancia
```

#### ¿Qué es una heurística?
Una **heurística** es una estimación inteligente que ayuda al algoritmo a decidir qué camino explorar primero.

#### Características de una buena heurística:
1. **Admisible**: Nunca debe sobreestimar el costo real
2. **Consistente**: h(n) ≤ costo(n, n') + h(n')
3. **Informativa**: Debe guiar hacia el objetivo

#### ¿Por qué distancia euclidiana?
- Es **admisible**: La línea recta siempre es el camino más corto
- Es **fácil de calcular**: Solo necesita las coordenadas
- Es **consistente**: Satisface la desigualdad triangular

**Ejemplo:**
```python
# Hospital (0,0) → Fábrica (12,8)
h(n) = √[(12-0)² + (8-0)²]
     = √[144 + 64]
     = √208
     ≈ 14.42 unidades

# Esta es nuestra estimación de la distancia restante
```

---

### 3️⃣ **Función Principal: buscar_ruta_optima()**

```python
def buscar_ruta_optima(inicio, objetivo):
```

Esta es la implementación completa del algoritmo A*. Vamos a desglosarla paso a paso:

#### **Paso 1: Inicialización**

```python
pasos = []
cola_prioridad = []
heapq.heappush(cola_prioridad, (0, inicio))
```

**¿Qué hace?**
- `pasos`: Lista para registrar cada iteración (para debugging)
- `cola_prioridad`: Heap con los nodos por explorar
- Insertamos el nodo inicial con prioridad 0

#### **Paso 2: Estructuras de Datos**

```python
origen_nodo = {}
origen_nodo[inicio] = None

costo_acumulado = {}
costo_acumulado[inicio] = 0
```

**origen_nodo (diccionario)**
- **Propósito**: Rastrear de dónde venimos
- **Uso**: Para reconstruir el camino al final
- **Ejemplo**: `origen_nodo['Bodega'] = 'Hospital'`

**costo_acumulado (diccionario)**
- **Propósito**: Guardar g(n) - el costo real desde el inicio
- **Uso**: Para calcular f(n) = g(n) + h(n)
- **Ejemplo**: `costo_acumulado['Bodega'] = 6`

#### **Paso 3: Bucle Principal**

```python
while cola_prioridad:
    _, nodo_actual = heapq.heappop(cola_prioridad)
```

**¿Qué hace?**
1. Mientras haya nodos por explorar
2. Sacar el nodo con menor f(n) de la cola
3. El `_` ignora la prioridad (solo nos interesa el nodo)

#### **Paso 4: Verificar si llegamos al objetivo**

```python
if nodo_actual == objetivo:
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

**¿Qué hace?**
1. Si llegamos al objetivo, **reconstruir el camino**
2. Empezar desde el objetivo y retroceder usando `origen_nodo`
3. Invertir el camino (estaba al revés)
4. Devolver el resultado exitoso

**Ejemplo de reconstrucción:**
```
objetivo = 'Fábrica'
origen_nodo = {
    'Fábrica': 'Almacén',
    'Almacén': 'Farmacia',
    'Farmacia': 'Bodega',
    'Bodega': 'Hospital',
    'Hospital': None
}

Reconstrucción:
1. Fábrica → origen_nodo['Fábrica'] = Almacén
2. Almacén → origen_nodo['Almacén'] = Farmacia
3. Farmacia → origen_nodo['Farmacia'] = Bodega
4. Bodega → origen_nodo['Bodega'] = Hospital
5. Hospital → origen_nodo['Hospital'] = None (FIN)

Camino invertido: ['Hospital', 'Bodega', 'Farmacia', 'Almacén', 'Fábrica']
```

#### **Paso 5: Explorar Vecinos**

```python
if nodo_actual in CONEXIONES:
    for conexion in CONEXIONES[nodo_actual]:
        vecino = conexion['destino']
        nuevo_costo = costo_acumulado[nodo_actual] + conexion['costo']
```

**¿Qué hace?**
1. Obtener todos los vecinos del nodo actual
2. Para cada vecino, calcular el costo de llegar ahí
3. `nuevo_costo` = lo que llevamos + costo de la arista

**Ejemplo:**
```
nodo_actual = 'Hospital'
costo_acumulado['Hospital'] = 0

Vecino 1: Bodega Central
- conexion['costo'] = 6
- nuevo_costo = 0 + 6 = 6

Vecino 2: Centro Distribución
- conexion['costo'] = 7
- nuevo_costo = 0 + 7 = 7
```

#### **Paso 6: Actualizar Costos**

```python
if vecino not in costo_acumulado or nuevo_costo < costo_acumulado[vecino]:
    costo_acumulado[vecino] = nuevo_costo
    prioridad = nuevo_costo + calcular_heuristica(vecino, objetivo)
    heapq.heappush(cola_prioridad, (prioridad, vecino))
    origen_nodo[vecino] = nodo_actual
```

**¿Qué hace?**
1. Si es la primera vez que visitamos el vecino, O
2. Si encontramos un camino más corto al vecino
3. Actualizar el costo acumulado
4. Calcular f(n) = g(n) + h(n)
5. Agregar a la cola con esta prioridad
6. Actualizar de dónde venimos

**Ejemplo completo:**
```
Explorando: Hospital → Bodega Central

g(n) = nuevo_costo = 6
h(n) = calcular_heuristica('Bodega', 'Fábrica')
     = √[(12-5)² + (8-3)²]
     = √[49 + 25]
     = √74 ≈ 8.6

f(n) = g(n) + h(n) = 6 + 8.6 = 14.6

heapq.heappush(cola_prioridad, (14.6, 'Bodega Central'))
origen_nodo['Bodega Central'] = 'Hospital'
costo_acumulado['Bodega Central'] = 6
```

---

## 📊 Ejemplo Práctico Paso a Paso

Vamos a trazar la ejecución completa de:
**Hospital → Fábrica de Insumos**

### Estado Inicial
```python
inicio = 'Hospital'
objetivo = 'Fabrica Insumos'

cola_prioridad = [(0, 'Hospital')]
costo_acumulado = {'Hospital': 0}
origen_nodo = {'Hospital': None}
```

---

### **Iteración 1: Explorar Hospital**

```
Nodo actual: Hospital
Coordenadas: (0, 0)
g(n) = 0

Vecinos:
1. Bodega Central
   - Costo arista: 6
   - g(n) = 0 + 6 = 6
   - h(n) = √[(12-5)² + (8-3)²] = 8.6
   - f(n) = 6 + 8.6 = 14.6

2. Centro Distribución
   - Costo arista: 7
   - g(n) = 0 + 7 = 7
   - h(n) = √[(12-3)² + (8-5)²] = 9.5
   - f(n) = 7 + 9.5 = 16.5

Cola de prioridad:
[(14.6, 'Bodega Central'), (16.5, 'Centro Distribución')]

Siguiente nodo a explorar: Bodega Central (menor f)
```

---

### **Iteración 2: Explorar Bodega Central**

```
Nodo actual: Bodega Central
Coordenadas: (5, 3)
g(n) = 6

Vecinos:
1. Hospital (ya visitado, costo mayor → ignorar)

2. Farmacia Principal
   - Costo arista: 4
   - g(n) = 6 + 4 = 10
   - h(n) = √[(12-7)² + (8-2)²] = 7.8
   - f(n) = 10 + 7.8 = 17.8
   - Agregar a la cola

3. Centro Distribución
   - Costo arista: 3
   - Nuevo g(n) = 6 + 3 = 9
   - g(n) anterior = 7 (desde Hospital directo)
   - Comparación: 9 > 7 → NO actualizar
   - El camino anterior (Hospital → Centro Dist) es mejor
   - Se mantiene costo_acumulado['Centro Distribución'] = 7

Cola de prioridad:
[(16.5, 'Centro Distribución'), (17.8, 'Farmacia Principal')]

Siguiente: Centro Distribución (f=16.5, con el costo óptimo de 7)
```

---

### **Iteración 3: Explorar Centro Distribución**

```
Nodo actual: Centro Distribución
Coordenadas: (3, 5)
g(n) = 7 (desde Hospital directo)

Vecinos:
1. Hospital (ya visitado → ignorar)

2. Bodega Central
   - Costo arista: 3
   - Nuevo g(n) = 7 + 3 = 10
   - g(n) anterior = 6 (desde Hospital)
   - 10 > 6 → NO actualizar (camino anterior es mejor)

3. Almacén Regional
   - Costo arista: 8
   - g(n) = 7 + 8 = 15
   - h(n) = √[(12-10)² + (8-6)²] = 2.8
   - f(n) = 15 + 2.8 = 17.8

Cola de prioridad actualizada:
[(17.8, 'Farmacia Principal'), (17.8, 'Almacén Regional')]

Siguiente: Farmacia Principal (menor f, o primero en la cola)
```

---

### **Iteración 4: Explorar Farmacia Principal**

```
Nodo actual: Farmacia Principal
Coordenadas: (7, 2)
g(n) = 10

Vecinos:
1. Bodega Central (ya visitado con mejor costo → ignorar)

2. Almacén Regional
   - Costo arista: 5
   - g(n) = 10 + 5 = 15
   - h(n) = √[(12-10)² + (8-6)²] = 2.8
   - f(n) = 15 + 2.8 = 17.8

Cola de prioridad:
[(17.8, 'Almacén Regional'), ...]

Siguiente: Almacén Regional
```

---

### **Iteración 5: Explorar Almacén Regional**

```
Nodo actual: Almacén Regional
Coordenadas: (10, 6)
g(n) = 15

Vecinos:
1. Centro Distribución (costo mayor → ignorar)
2. Farmacia Principal (ya visitado → ignorar)

3. Fábrica Insumos ← ¡OBJETIVO!
   - Costo arista: 4
   - g(n) = 15 + 4 = 19
   - ¡Llegamos al objetivo!
```

---

### **Resultado Final**

```python
{
    'exito': True,
    'camino': ['Hospital', 'Bodega Central', 'Farmacia Principal', 
               'Almacén Regional', 'Fábrica Insumos'],
    'costo_total': 19,
    'pasos': [
        {'paso': 1, 'nodo_explorado': 'Hospital', ...},
        {'paso': 2, 'nodo_explorado': 'Bodega Central', ...},
        {'paso': 3, 'nodo_explorado': 'Centro Distribución', ...},
        {'paso': 4, 'nodo_explorado': 'Farmacia Principal', ...},
        {'paso': 5, 'nodo_explorado': 'Almacén Regional', ...},
    ]
}
```

**Visualización del camino:**
```
Hospital (0,0)
    ↓ [costo: 6]
Bodega Central (5,3)
    ↓ [costo: 4]
Farmacia Principal (7,2)
    ↓ [costo: 5]
Almacén Regional (10,6)
    ↓ [costo: 4]
Fábrica Insumos (12,8)

COSTO TOTAL: 6 + 4 + 5 + 4 = 19 km
```

---

## 🎯 Casos de Uso

### 1. **Distribución de Insumos Médicos**
```
Escenario: Enviar medicamentos urgentes desde el Hospital a la Fábrica
Solución: A* encuentra la ruta más rápida (19 km)
Beneficio: Ahorro de tiempo y combustible
```

### 2. **Comparación de Rutas**
```python
# En views.py se calculan rutas alternativas
rutas_alternativas = []
for ubicacion in ubicaciones:
    ruta1 = buscar_ruta_optima(origen, ubicacion)
    ruta2 = buscar_ruta_optima(ubicacion, destino)
    costo_total = ruta1['costo_total'] + ruta2['costo_total']
```

### 3. **Optimización Logística**
- Planificación de entregas diarias
- Cálculo de costos operativos
- Visualización de eficiencia de rutas

---

## 🔬 Análisis de Complejidad

### Complejidad Temporal
```
O(b^d) en el peor caso
Donde:
- b = factor de ramificación (número promedio de vecinos)
- d = profundidad de la solución

Con buena heurística: O(b*d) en casos prácticos
```

### Complejidad Espacial
```
O(b^d) - Debe guardar todos los nodos en memoria
```

### Comparación con otros algoritmos:

| Algoritmo | Tiempo | Espacio | Óptimo | Heurística |
|-----------|--------|---------|--------|------------|
| **A*** | O(b*d) | O(b^d) | ✅ Sí | ✅ Sí |
| BFS | O(b^d) | O(b^d) | ✅ Sí* | ❌ No |
| DFS | O(b^m) | O(bm) | ❌ No | ❌ No |
| Dijkstra | O(n²) | O(n) | ✅ Sí | ❌ No |
| Greedy | O(n log n) | O(n) | ❌ No | ✅ Sí |

*BFS es óptimo solo para grafos no ponderados

---

## 📖 Referencias y Recursos

### Papers Originales
- Hart, P. E.; Nilsson, N. J.; Raphael, B. (1968). "A Formal Basis for the Heuristic Determination of Minimum Cost Paths"

### Aplicaciones Reales
- **Google Maps**: Usa variantes de A* para rutas
- **Videojuegos**: Movimiento de NPCs (Ej: Age of Empires, StarCraft)
- **Robótica**: Navegación autónoma
- **Logística**: Amazon, DHL, FedEx

### Mejoras y Variantes
- **IDA***: Iterative Deepening A* (menos memoria)
- **SMA***: Simplified Memory-bounded A*
- **D***: Dynamic A* (para entornos cambiantes)
- **Jump Point Search**: Optimización para grids uniformes

---

## 🎓 Conclusión

El módulo de rutas implementa A* de forma completa y eficiente, aprovechando:

1. ✅ **heapq** para gestión eficiente de la cola de prioridad
2. ✅ **math.sqrt()** para cálculo preciso de la heurística euclidiana
3. ✅ Estructuras de datos (diccionarios) para rastrear costos y orígenes
4. ✅ Función f(n) = g(n) + h(n) que balancea costo real y estimación

**Resultado**: Un sistema robusto que encuentra la ruta óptima entre ubicaciones médicas, optimizando tiempo y recursos en la distribución de insumos.

---

## 📞 Preguntas Frecuentes

### ¿Por qué no usar simplemente Dijkstra?
A* es más rápido porque la heurística guía la búsqueda hacia el objetivo, evitando explorar nodos innecesarios.

### ¿La heurística puede ser cualquier función?
No, debe ser **admisible** (nunca sobreestimar) para garantizar optimalidad.

### ¿Qué pasa si hay ciclos en el grafo?
A* los maneja correctamente gracias a `costo_acumulado`, que evita revisar nodos con peor costo.

### ¿Se puede usar para más de 6 ubicaciones?
¡Sí! Solo agregar más nodos a `UBICACIONES` y `CONEXIONES`.

---

**Autor**: Sistema de Salud - Módulo de Optimización de Rutas  
**Fecha**: Noviembre 2025  
**Versión**: 1.0
