from django.urls import path
from .views import (
    index,
    lista_libros, crear_libro,
    lista_autores, crear_autor,
    lista_prestamos, crear_prestamo, detalle_prestamo,
    lista_multas, crear_multa, detalle_multa,
)

urlpatterns = [
    path('', index, name='index'),

    # Libros
    path('libros/', lista_libros, name='lista_libros'),
    path('libros/nuevo/', crear_libro, name='crear_libro'),

    # Autores
    path('autores/', lista_autores, name='lista_autores'),
    path('autores/nuevo/', crear_autor, name='crear_autor'),

    # Préstamos
    path('prestamos/', lista_prestamos, name='lista_prestamos'),
    path('prestamos/nuevo/', crear_prestamo, name='crear_prestamo'),
    path('prestamos/<int:id>/', detalle_prestamo, name='detalle_prestamo'),

    # Multas
    path('multas/', lista_multas, name='lista_multas'),
    path('multas/nuevo/', crear_multa, name='crear_multa'),
    path('multas/<int:id>/', detalle_multa, name='detalle_multa'),
]

