from django.urls import path
from .views import *


urlpatternss =[
    path ("",index, name="index")

    #libros
    path('libro/',lista_libros, name="lista_libros"),
    path('libros/nuevo/',crear_libro, name="crear_libro"),

    #autores 
    path('autores/',lista_autores, name="lista_autores"),
    path('autores/nuevo/',crear_autor, name="crear_autores")

    #prestamo
    path ('prestamo/',lista_Prestamos, name="lista_prestamos")
    path('prestamo/nuevo/', crear_prestamo, name="crear_prestamo")
    path('prestamo/<int:id>',detalle_prestamo,name="detalle_prestamo")

    #Multa
    path ('multa/',lista_Multas, name="lista_multas")
    path('multa/nuevo/', crear_multa, name="crear_multa")
    path('multa/<int:id>',detalle_multa,name="detalle_multa")
]

