from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Autor, Libro, Prestamo, Multa

def index(request):
    titulo2 = "Hola Mundo"
    title = settings.TITLE
    # 'gestion/templates/home.html' in guide, simplified to 'home.html' for standard app dirs
    return render(request, 'home.html', {'titulo': title, 't': titulo2})

# Libros
def lista_libros(request):
    libros = Libro.objects.all()
    # 'gestion/templates/libros.html' in guide, simplified to 'libros.html'
    return render(request, 'libros.html', {'libros': libros})

def crear_libro(request):
    autores = Autor.objects.all()
    if request.method == "POST":
        titulo = request.POST.get('titulo')
        autor_id = request.POST.get('autor')
        
        if titulo and autor_id:
             # Logic from image seems to imply direct creation or just missing the create call in the snippet?
             # The image shows 'if titulo and autor_id:'.
             # Wait, the image snippet for crear_libro is cut off at 'if titulo and autor_id:'.
             # I will assume standard creation logic or what I had before, but adapted to variables.
             # Actually previous logic was robust. I will keep it robust but use the new variables.
             
             
             autor_obj = get_object_or_404(Autor, id=autor_id)
             disponible = request.POST.get('disponible') == 'on'
             Libro.objects.create(titulo=titulo, autor=autor_obj, disponible=disponible)
             return redirect('lista_libros')
             
    return render(request, 'crear_libros.html', {'autores': autores})

# Autores
def lista_autores(request):
    autores = Autor.objects.all()
    return render(request, 'autores.html', {'autores': autores})

def criar_autor(request, id=None): # Typo in my thought but likely intentional reuse.
# Wait, checking image again.
# The image row 25: path('autores/<int:id>/editar/', crear_autor, name="editar_autor")
# So 'crear_autor' view must accept 'id'.
def crear_autor(request, id=None):
    if id:
        autor_obj = get_object_or_404(Autor, id=id)
    else:
        autor_obj = None

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        bibliografia = request.POST.get('bibliografia', '').strip()

        if not nombre or not apellido or not bibliografia:
            messages.error(request, 'Por favor completa todos los campos.')
            return render(request, 'crear_autores.html', {
                'nombre': nombre,
                'apellido': apellido,
                'bibliografia': bibliografia,
                'autor': autor_obj 
            })

        if autor_obj:
            autor_obj.nombre = nombre
            autor_obj.apellido = apellido
            autor_obj.bibliografia = bibliografia
            autor_obj.save()
            messages.success(request, 'Autor actualizado correctamente.')
        else:
            Autor.objects.create(nombre=nombre, apellido=apellido, bibliografia=bibliografia)
            messages.success(request, 'Autor creado correctamente.')
            
        return redirect('lista_autores')

    context = {}
    if autor_obj:
        context = {
            'nombre': autor_obj.nombre,
            'apellido': autor_obj.apellido,
            'bibliografia': autor_obj.bibliografia,
            'autor': autor_obj,
            'texto_boton': 'Guardar cambios'
        }
    
    return render(request, 'crear_autores.html', context)

# Prestamos
def lista_prestamos(request):
    prestamos = Prestamo.objects.all()
    return render(request, 'prestamos.html', {'prestamos': prestamos})

@login_required
def crear_prestamo(request):
    if not request.user.has_perm('gestion.gestionar_prestamos'):
        return HttpResponseForbidden()
    
    libro = Libro.objects.filter(disponible=True)
    usuario = User.objects.all()

    if request.method == 'POST':
        libro_id = request.POST.get('libro')
        usuario_id = request.POST.get('usuario')
        fecha_prestamo = request.POST.get('fecha_prestamo')
        
        if libro_id and usuario_id and fecha_prestamo:
            libro = get_object_or_404(Libro, id=libro_id)
            usuario = get_object_or_404(User, id=usuario_id)
            
            
            prestamo = Prestamo.objects.create(
                libro=libro,
                usuario=usuario,
                fecha_prestamo=fecha_prestamo
            )
            
            libro.disponible = False
            libro.save()
            return redirect('detalle_prestamo', id=prestamo.id)

    # In case of GET or invalid form, correct handling in the image is not fully visible but we should return the context keys it seems to want. 
    # Based on the image code 'context' variable logic seems to be what was replaced.
    # The image cuts off the 'else' or return block but shows 'return render(..., context)' at the top for some other function maybe?
    # I will adapt the existing context return to be cleaner.
    
    # In case of GET or invalid form
    fecha = (timezone.now().date()).isoformat() # YYYY-MM-DD
    return render(request, 'crear_prestamos.html', {
        'libros': libro, 
        'usuarios': usuario,
        'fecha': fecha
    })

def detalle_prestamo(request, id):
    prestamo = get_object_or_404(Prestamo, id=id)
    return render(request, 'detalle_prestamo.html', {'prestamo': prestamo})

# Multas
def lista_multas(request):
    multas = Multa.objects.all()
    return render(request, 'multas.html', {'multas': multas})

def crear_multa(request):
    prestamos = Prestamo.objects.all()
    if request.method == 'POST':
        prestamo_id = request.POST.get('prestamo')
        tipo = request.POST.get('tipo')
        monto = request.POST.get('monto')

        if prestamo_id and tipo and monto:
            prestamo = get_object_or_404(Prestamo, id=prestamo_id)
            Multa.objects.create(prestamo=prestamo, tipo=tipo, monto=monto)
            return redirect('lista_multas')

    return render(request, 'crear_multa.html', {'prestamos': prestamos})

def detalle_multa(request, id):
    multa = get_object_or_404(Multa, id=id)
    return render(request, 'detalle_multa.html', {'multa': multa})

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})
