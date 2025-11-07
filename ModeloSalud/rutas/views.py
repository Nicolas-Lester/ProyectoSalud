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
        
        # Obtener ubicaciones para el formulario
        ubicaciones = algoritmo_busqueda.obtener_ubicaciones()
        
        context = {
            'ubicaciones': ubicaciones,
            'resultado': resultado,
            'origen': origen,
            'destino': destino,
        }
        return render(request, 'rutas/home.html', context)
    
    # Si no es POST, redirigir a la pagina principal
    return home_rutas(request)
