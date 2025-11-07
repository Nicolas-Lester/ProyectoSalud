from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_rutas, name='rutas_home'),
    path('calcular/', views.calcular_ruta, name='calcular_ruta'),
]
