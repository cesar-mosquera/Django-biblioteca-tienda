from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Libro, autor, Prestamo, Multa

# Vistas según la guía del profesor
def index(request):
    return render(request, 'index.html', {})

# Libros
def lista_libros(request):
    libros = Libro.objects.all()
    return render(request, 'libros.html', {'libros': libros})

def crear_libro(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        autor_id = request.POST.get('autor')
        disponible = request.POST.get('disponible', '').lower() == 'on'

        if not titulo or not autor_id:
            messages.error(request, 'Por favor completa todos los campos requeridos.')
            autores_list = autor.objects.all()
            return render(request, 'crear_libros.html', {
                'titulo': titulo,
                'autor_id': autor_id,
                'autores': autores_list,
            })

        try:
            autor_obj = autor.objects.get(id=autor_id)
            Libro.objects.create(titulo=titulo, autor=autor_obj, disponible=disponible)
            messages.success(request, 'Libro creado correctamente.')
            return redirect('lista_libros')
        except autor.DoesNotExist:
            messages.error(request, 'El autor seleccionado no existe.')
            autores_list = autor.objects.all()
            return render(request, 'crear_libros.html', {
                'titulo': titulo,
                'autor_id': autor_id,
                'autores': autores_list,
            })

    autores_list = autor.objects.all()
    return render(request, 'crear_libros.html', {'autores': autores_list})

# Autores
def lista_autores(request):
    autores = autor.objects.all()
    return render(request, 'autores.html', {'autores': autores})

def crear_autor(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        bibliografia = request.POST.get('bibliografia', '').strip()

        if not nombre or not apellido or not bibliografia:
            messages.error(request, 'Por favor completa todos los campos.')
            # Re-render con los datos ingresados
            return render(request, 'crear_autores.html', {
                'nombre': nombre,
                'apellido': apellido,
                'bibliografia': bibliografia,
            })

        autor.objects.create(nombre=nombre, apellido=apellido, bibliografia=bibliografia)
        messages.success(request, 'Autor creado correctamente.')
        return redirect('lista_autores')

    return render(request, 'crear_autores.html', {})

# Prestamos
def lista_prestamos(request):
    prestamos = Prestamo.objects.all()
    return render(request, 'prestamos.html', {'prestamos': prestamos})

def crear_prestamo(request):
    if request.method == 'POST':
        libro_id = request.POST.get('libro')
        usuario_id = request.POST.get('usuario')
        fecha_max_str = request.POST.get('fecha_max', '').strip()

        if not libro_id or not usuario_id or not fecha_max_str:
            messages.error(request, 'Por favor completa todos los campos requeridos.')
            libros_list = Libro.objects.filter(disponible=True)
            usuarios_list = User.objects.all()
            return render(request, 'crear_prestamos.html', {
                'libros': libros_list,
                'usuarios': usuarios_list,
            })

        try:
            libro_obj = Libro.objects.get(id=libro_id)
            usuario_obj = User.objects.get(id=usuario_id)

            if not libro_obj.disponible:
                messages.error(request, 'El libro no está disponible.')
                libros_list = Libro.objects.filter(disponible=True)
                usuarios_list = User.objects.all()
                return render(request, 'crear_prestamos.html', {
                    'libros': libros_list,
                    'usuarios': usuarios_list,
                })

            fecha_max = timezone.datetime.strptime(fecha_max_str, '%Y-%m-%d').date()
            Prestamo.objects.create(
                libro=libro_obj,
                usuario=usuario_obj,
                fecha_prestamo=timezone.now().date(),
                fecha_max=fecha_max,
            )
            libro_obj.disponible = False
            libro_obj.save()

            messages.success(request, 'Préstamo creado correctamente.')
            return redirect('lista_prestamos')
        except (Libro.DoesNotExist, User.DoesNotExist):
            messages.error(request, 'Libro o usuario no encontrado.')
        except ValueError:
            messages.error(request, 'Formato de fecha inválido. Usa YYYY-MM-DD.')

        libros_list = Libro.objects.filter(disponible=True)
        usuarios_list = User.objects.all()
        return render(request, 'crear_prestamos.html', {
            'libros': libros_list,
            'usuarios': usuarios_list,
        })

    libros_list = Libro.objects.filter(disponible=True)
    usuarios_list = User.objects.all()
    return render(request, 'crear_prestamos.html', {
        'libros': libros_list,
        'usuarios': usuarios_list,
    })

def detalle_prestamo(request, id):
    return HttpResponse(f"Detalle prestamo {id}")

# Multas
def lista_multas(request):
    multas = Multa.objects.all()
    return render(request, 'multas.html', {'multas': multas})

def crear_multa(request):
    return HttpResponse("Crear multa")

def detalle_multa(request, id):
    return HttpResponse(f"Detalle multa {id}")
