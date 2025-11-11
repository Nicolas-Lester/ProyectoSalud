from django.shortcuts import render, redirect
from django.contrib import messages
from .models import DemandaPacientes
from . import modelo_prediccion
import pandas as pd
from datetime import datetime, timedelta


# Vista principal de prediccion de demanda
def home_prediccion(request):
    """
    Muestra el dashboard de prediccion de demanda
    """
    # Ver si el modelo esta entrenado
    modelo, _ = modelo_prediccion.cargar_modelo_prediccion()
    modelo_entrenado = modelo is not None
    
    # Obtener estadisticas de datos historicos
    total_registros = DemandaPacientes.objects.count()
    
    # Ultimos 7 dias de datos
    ultimos_registros = DemandaPacientes.objects.all()[:7]
    
    context = {
        'modelo_entrenado': modelo_entrenado,
        'total_registros': total_registros,
        'ultimos_registros': ultimos_registros,
    }
    return render(request, 'prediccion/home.html', context)


# Vista para generar datos de ejemplo
def generar_datos(request):
    """
    Genera datos historicos de ejemplo para entrenar
    """
    if request.method == 'POST':
        try:
            # Generar datos
            cantidad = modelo_prediccion.generar_datos_ejemplo()
            messages.success(request, f'Se generaron {cantidad} registros historicos de ejemplo')
        except Exception as e:
            messages.error(request, f'Error al generar datos: {str(e)}')
        
        return redirect('prediccion_home')
    
    return render(request, 'prediccion/generar_datos.html')


# Vista para entrenar el modelo
def entrenar_prediccion(request):
    """
    Entrena el modelo de prediccion con los datos historicos
    """
    if request.method == 'POST':
        # Obtener datos historicos
        registros = DemandaPacientes.objects.all()
        
        if registros.count() < 10:
            messages.error(request, 'Necesitas al menos 10 registros para entrenar. Genera datos primero.')
            return redirect('prediccion_home')
        
        # Convertir a DataFrame
        datos = list(registros.values('dia_semana', 'mes', 'es_feriado', 'pacientes'))
        df = pd.DataFrame(datos)
        
        # Entrenar modelo
        resultado = modelo_prediccion.entrenar_modelo_prediccion(df)
        
        if resultado['ok']:
            score_porcentaje = resultado['score'] * 100
            messages.success(
                request,
                f'Modelo entrenado exitosamente. Precisión: {score_porcentaje:.1f}%'
            )
            
            # Pasar los gráficos a la plantilla
            context = {
                'resultado': resultado,
                'entrenado': True
            }
            return render(request, 'prediccion/entrenar.html', context)
        else:
            messages.error(request, resultado.get('error', 'Error al entrenar'))
            return redirect('prediccion_home')
    
    return render(request, 'prediccion/entrenar.html')


# Vista para hacer predicciones
def hacer_prediccion(request):
    """
    Permite predecir demanda para fechas futuras
    """
    predicciones = []
    
    if request.method == 'POST':
        fecha_str = request.POST.get('fecha')
        es_feriado = request.POST.get('es_feriado') == 'on'
        tipo = request.POST.get('tipo', 'dia')  # 'dia' o 'semana'
        
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
            
            if tipo == 'dia':
                # Prediccion para un solo dia
                resultado = modelo_prediccion.predecir_demanda(fecha, es_feriado)
                if resultado['ok']:
                    predicciones.append(resultado)
                else:
                    messages.error(request, resultado['error'])
            
            elif tipo == 'semana':
                # Prediccion para una semana completa
                for i in range(7):
                    fecha_dia = fecha + timedelta(days=i)
                    resultado = modelo_prediccion.predecir_demanda(fecha_dia, es_feriado)
                    if resultado['ok']:
                        predicciones.append(resultado)
        
        except ValueError:
            messages.error(request, 'Formato de fecha inválido')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    context = {
        'predicciones': predicciones
    }
    return render(request, 'prediccion/predecir.html', context)


# Vista para ver historico
def ver_historico(request):
    """
    Muestra el historico de demanda de pacientes
    """
    registros = DemandaPacientes.objects.all()[:30]  # Ultimos 30 dias
    
    # Calcular estadisticas
    if registros:
        pacientes_list = [r.pacientes for r in registros]
        promedio = sum(pacientes_list) / len(pacientes_list)
        maximo = max(pacientes_list)
        minimo = min(pacientes_list)
    else:
        promedio = maximo = minimo = 0
    
    context = {
        'registros': registros,
        'promedio': round(promedio, 1),
        'maximo': maximo,
        'minimo': minimo,
    }
    return render(request, 'prediccion/historico.html', context)
