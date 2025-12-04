from django.shortcuts import render, redirect, get_object_or_404
from dyango.contrib.auth.decorators import login_required
from dyango.contrib.auth.models import User
from dyango.utils import timezone

from .models import Autor, Libro, Prestamo, Multa

def index(resquest):
    title = settings.TITLE
    return render(request, 'gestion/template/index.html',{'titulo':title, 't': titulo2})

def lista_Libros(request):
    libros = Libro.objects.all()
    return render(request, 'gestion/templates/libros.html', {'libros': libros})

def crear_Libro (request):
    pass

def lista_Autores(request):
    autores = Autor.objects.all()
    return render(request, 'gestion/templates/autores.html', {'autores': autores})


def crear_Autor (request):
    pass

def lista_Prestamos(request):
    prestamos = Prestamo.objects.all()
    return render(request, 'gestion/templates/prestamos.html', {'prestamos': prestamos})

def crear_Prestamo (request):
    pass

def lista_Multas(request):
    multas = Multa.objects.all()
    return render(request, 'gestion/templates/multas.html', {'multas': multas})

def crear_Multa (request):
    pass

