"""URLs de la aplicación galería."""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('proyectos/', views.lista_proyectos, name='lista_proyectos'),
    path('proyectos/<slug:slug>/', views.detalle_proyecto, name='detalle_proyecto'),
    path('sobre-mi/', views.sobre_mi, name='sobre_mi'),
    path('contacto/', views.contacto, name='contacto'),
]
