# Algoritmo A* para encontrar la ruta optima de insumos medicos
# Utiliza un grafo con heuristica para optimizar la busqueda

import heapq
import math

# Definir el grafo de ubicaciones (nodos) y sus conexiones (aristas)
# Cada ubicacion tiene coordenadas X,Y para calcular la heuristica
UBICACIONES = {
    'Hospital': {'x': 0, 'y': 0},
    'Bodega Central': {'x': 5, 'y': 3},
    'Centro Distribucion': {'x': 3, 'y': 5},
    'Farmacia Principal': {'x': 7, 'y': 2},
    'Almacen Regional': {'x': 10, 'y': 6},
    'Fabrica Insumos': {'x': 12, 'y': 8},
}

# Conexiones entre ubicaciones con sus distancias (costo real)
# Representa las rutas disponibles y el tiempo/distancia entre ellas
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
    'Centro Distribucion': [
        {'destino': 'Hospital', 'costo': 7},
        {'destino': 'Bodega Central', 'costo': 3},
        {'destino': 'Almacen Regional', 'costo': 8},
    ],
    'Farmacia Principal': [
        {'destino': 'Bodega Central', 'costo': 4},
        {'destino': 'Almacen Regional', 'costo': 5},
    ],
    'Almacen Regional': [
        {'destino': 'Centro Distribucion', 'costo': 8},
        {'destino': 'Farmacia Principal', 'costo': 5},
        {'destino': 'Fabrica Insumos', 'costo': 4},
    ],
    'Fabrica Insumos': [
        {'destino': 'Almacen Regional', 'costo': 4},
    ],
}


# Funcion para calcular la heuristica (distancia estimada)
# Usa distancia euclidiana entre dos puntos
def calcular_heuristica(origen, destino):
    """
    Calcula la distancia en linea recta entre dos ubicaciones
    Esto ayuda al algoritmo a priorizar caminos prometedores
    """
    x1, y1 = UBICACIONES[origen]['x'], UBICACIONES[origen]['y']
    x2, y2 = UBICACIONES[destino]['x'], UBICACIONES[destino]['y']
    
    # Formula de distancia euclidiana: raiz((x2-x1)^2 + (y2-y1)^2)
    distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distancia


# Algoritmo A* para buscar la ruta mas corta
def buscar_ruta_optima(inicio, objetivo):
    """
    Implementacion del algoritmo A* (A estrella)
    Encuentra el camino mas corto entre dos ubicaciones
    
    Parametros:
    - inicio: ubicacion de partida
    - objetivo: ubicacion de destino
    
    Retorna:
    - camino: lista con las ubicaciones en orden
    - costo_total: distancia/tiempo total del recorrido
    - pasos: lista con detalles de cada paso del algoritmo
    """
    
    # Lista de pasos para mostrar como funciona el algoritmo
    pasos = []
    
    # Cola de prioridad: guarda nodos a explorar ordenados por f(n) = g(n) + h(n)
    # f(n) = costo total estimado, g(n) = costo real, h(n) = heuristica
    cola_prioridad = []
    heapq.heappush(cola_prioridad, (0, inicio))
    
    # Diccionario para guardar de donde venimos (para reconstruir el camino)
    origen_nodo = {}
    origen_nodo[inicio] = None
    
    # Diccionario con el costo real desde el inicio hasta cada nodo
    costo_acumulado = {}
    costo_acumulado[inicio] = 0
    
    paso_numero = 1
    
    # Mientras haya nodos por explorar
    while cola_prioridad:
        # Sacar el nodo con menor f(n) de la cola
        _, nodo_actual = heapq.heappop(cola_prioridad)
        
        # Registrar este paso
        pasos.append({
            'paso': paso_numero,
            'nodo_explorado': nodo_actual,
            'costo_acumulado': costo_acumulado[nodo_actual],
            'heuristica': calcular_heuristica(nodo_actual, objetivo),
        })
        paso_numero += 1
        
        # Si llegamos al objetivo, reconstruir el camino
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
        
        # Explorar vecinos del nodo actual
        if nodo_actual in CONEXIONES:
            for conexion in CONEXIONES[nodo_actual]:
                vecino = conexion['destino']
                nuevo_costo = costo_acumulado[nodo_actual] + conexion['costo']
                
                # Si encontramos un camino mejor a este vecino
                if vecino not in costo_acumulado or nuevo_costo < costo_acumulado[vecino]:
                    costo_acumulado[vecino] = nuevo_costo
                    # f(n) = g(n) + h(n)
                    prioridad = nuevo_costo + calcular_heuristica(vecino, objetivo)
                    heapq.heappush(cola_prioridad, (prioridad, vecino))
                    origen_nodo[vecino] = nodo_actual
    
    # Si no se encontro camino
    return {
        'exito': False,
        'error': 'No se encontró una ruta entre las ubicaciones',
        'pasos': pasos
    }


# Funcion para obtener todas las ubicaciones disponibles
def obtener_ubicaciones():
    """
    Retorna la lista de todas las ubicaciones del grafo
    """
    return list(UBICACIONES.keys())
