from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_prediccion, name='prediccion_home'),
    path('generar-datos/', views.generar_datos, name='generar_datos'),
    path('entrenar/', views.entrenar_prediccion, name='entrenar_prediccion'),
    path('predecir/', views.hacer_prediccion, name='hacer_prediccion'),
    path('historico/', views.ver_historico, name='ver_historico'),
]
