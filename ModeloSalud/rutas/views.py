from django.shortcuts import render
from . import algoritmo_busqueda


# Vista principal de optimizacion de rutas
def home_rutas(request):
    """
    Muestra la pagina principal con el formulario para calcular rutas
    """
    # Obtener todas las ubicaciones disponibles
    ubicaciones = algoritmo_busqueda.obtener_ubicaciones()
    
    context = {
        'ubicaciones': ubicaciones,
    }
    return render(request, 'rutas/home.html', context)


# Vista para calcular la ruta optima
def calcular_ruta(request):
    """
    Calcula la ruta mas corta usando el algoritmo A*
    """
    if request.method == 'POST':
        # Obtener origen y destino del formulario
        origen = request.POST.get('origen')
        destino = request.POST.get('destino')
        
        # Validar que no sean iguales
        if origen == destino:
            ubicaciones = algoritmo_busqueda.obtener_ubicaciones()
            context = {
                'ubicaciones': ubicaciones,
                'error': 'El origen y destino deben ser diferentes'
            }
            return render(request, 'rutas/home.html', context)
        
        # Ejecutar el algoritmo A*
        resultado = algoritmo_busqueda.buscar_ruta_optima(origen, destino)
        
        # Calcular todas las rutas alternativas para comparación
        ubicaciones = algoritmo_busqueda.obtener_ubicaciones()
        rutas_alternativas = []
        
        if resultado['exito']:
            for ubicacion in ubicaciones:
                if ubicacion != origen and ubicacion != destino:
                    # Calcular ruta pasando por esta ubicación intermedia
                    ruta1 = algoritmo_busqueda.buscar_ruta_optima(origen, ubicacion)
                    ruta2 = algoritmo_busqueda.buscar_ruta_optima(ubicacion, destino)
                    
                    if ruta1['exito'] and ruta2['exito']:
                        costo_total = ruta1['costo_total'] + ruta2['costo_total']
                        # Combinar caminos eliminando duplicados
                        camino_completo = ruta1['camino'] + ruta2['camino'][1:]
                        rutas_alternativas.append({
                            'via': ubicacion,
                            'costo': costo_total,
                            'camino': camino_completo
                        })
            
            # Ordenar por costo
            rutas_alternativas.sort(key=lambda x: x['costo'])
        
        context = {
            'ubicaciones': ubicaciones,
            'resultado': resultado,
            'origen': origen,
            'destino': destino,
            'rutas_alternativas': rutas_alternativas,
        }
        return render(request, 'rutas/home.html', context)
    
    # Si no es POST, redirigir a la pagina principal
    return home_rutas(request)
