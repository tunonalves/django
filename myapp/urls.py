from django.urls import path 
from .           import views 

urlpatterns = [ 
 path("", views.index, name="index"),
 path("index2", views.index2, name="index2"),
 path("contactos", views.contactos, name="contactos"),
 path("cursos", views.cursos, name="cursos"), 
 path("curso/<str:nombre_curso>", views.curso, name="curso"), 
 path("cursos_api", views.cursos_api, name="cursos_api"), 
 path("cotizacion", views.cotizacion, name="cotizacion"), 
 path("aeropuertos", views.aeropuertos, name="aeropuertos"), 
 path("aeropuertos_json", views.aeropuertos_json, name="aeropuertos_json"),
] 