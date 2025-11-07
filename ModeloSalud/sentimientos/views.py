from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Comment
from . import servicios
import pandas as pd


# Vista de la pagina principal
def home(request):
    # Contar comentarios
    total = Comment.objects.count()
    positivos = Comment.objects.filter(etiqueta="positivo").count()
    negativos = Comment.objects.filter(etiqueta="negativo").count()
    
    # Ver si el modelo esta entrenado
    modelo, _ = servicios.cargar_modelo()
    modelo_entrenado = modelo is not None
    
    # Enviar datos a la plantilla
    context = {
        'total': total,
        'positivos': positivos,
        'negativos': negativos,
        'modelo_entrenado': modelo_entrenado,
    }
    return render(request, 'sentimientos/home.html', context)


# Vista para entrenar el modelo
def entrenar(request):
    if request.method == 'POST':
        # Obtener todos los comentarios de la base de datos
        comentarios = Comment.objects.all()
        
        # Verificar que haya suficientes comentarios
        if comentarios.count() < 10:
            messages.error(request, 'Necesitas al menos 10 comentarios para entrenar el modelo.')
            return redirect('home')
        
        # Convertir comentarios a formato DataFrame (tabla)
        datos = list(comentarios.values('texto', 'etiqueta'))
        df = pd.DataFrame(datos)
        
        # Entrenar el modelo
        resultado = servicios.entrenar_modelo(df)
        
        # Mostrar mensaje de exito con la precision
        precision = resultado["accuracy_test"]
        messages.success(request, f'Modelo entrenado exitosamente. Precisión: {precision:.2%}')
        return redirect('home')
    
    # Si no es POST, mostrar la pagina
    return render(request, 'sentimientos/entrenar.html')


# Vista para predecir el sentimiento de un texto
def predecir(request):
    resultado = None
    
    if request.method == 'POST':
        # Obtener el texto ingresado por el usuario
        texto = request.POST.get('texto', '')
        
        # Verificar que no este vacio
        if texto.strip():
            # Hacer la prediccion
            resultado = servicios.predecir(texto)
            
            # Si hay error, mostrar mensaje
            if not resultado.get('ok'):
                messages.error(request, resultado.get('error', 'Error desconocido'))
        else:
            messages.warning(request, 'Por favor ingresa un texto.')
    
    # Mostrar la pagina con el resultado
    context = {'resultado': resultado}
    return render(request, 'sentimientos/predecir.html', context)




# Vista para buscar comentarios por texto o filtrar por sentimiento
def buscar(request):
    # Obtener todos los comentarios ordenados del mas nuevo al mas viejo
    comentarios = Comment.objects.all().order_by('-id')
    
    # Obtener parametros de busqueda del formulario
    query = request.GET.get('q', '')
    filtro = request.GET.get('filtro', '')
    
    # Si hay texto de busqueda, filtrar comentarios
    if query:
        comentarios = comentarios.filter(texto__icontains=query)
    
    # Si eligieron un filtro (positivo o negativo), aplicarlo
    if filtro in ['positivo', 'negativo']:
        comentarios = comentarios.filter(etiqueta=filtro)
    
    # Enviar resultados a la pagina
    context = {
        'comentarios': comentarios,
        'query': query,
        'filtro': filtro,
    }
    return render(request, 'sentimientos/buscar.html', context)





# Vista para mostrar la lista de todos los comentarios
def listar_comentarios(request):
    # Traer los ultimos 100 comentarios de la base de datos
    # Se ordenan del mas reciente al mas antiguo con -id
    comentarios = Comment.objects.all().order_by('-id')[:100]
    
    # Mostrar en la pagina
    context = {'comentarios': comentarios}
    return render(request, 'sentimientos/listar.html', context)

