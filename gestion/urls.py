from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    index,
    lista_libros, crear_libro,
    lista_autores, crear_autor, editar_autor,
    lista_prestamos, crear_prestamo, detalle_prestamo,
    lista_multas, crear_multa, detalle_multa,
    registro,
)

urlpatterns = [
    path("", index, name="index"),

    # Gestión usuarios (según ejemplo del docente)
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('registro/', registro, name='registro'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Cambio de contraseña
    path('password/change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # Libros
    path('libros/', lista_libros, name='lista_libros'),
    path('libros/nuevo/', crear_libro, name='crear_libro'),

    #Autores
    path('autores/', lista_autores, name="lista_autores"),
    path('autores/nuevo/', crear_autor, name="crear_autores"),
    path('autores/<int:id>/editar/', crear_autor, name="editar_autor"),

    # Préstamos
    path('prestamos/', lista_prestamos, name='lista_prestamos'),
    path('prestamos/nuevo/', crear_prestamo, name='crear_prestamo'),
    path('prestamos/<int:id>/', detalle_prestamo, name='detalle_prestamo'),

    # Multas
    path('multas/', lista_multas, name='lista_multas'),
    path('multas/nuevo/', crear_multa, name='crear_multa'),
    path('multas/<int:id>/', detalle_multa, name='detalle_multa'),
]

