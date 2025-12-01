from django.db import models

# Create your models here.

class autor(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
class Libro(models.Model):
    titulo = models.CharField(max_length=20)
    autor = models.ForeignKey(autor, related_name="libros")
    disponible = models.BooleanField(default=True)

    def __str__(self):
            return self.titulo
        
class Prestamo(models.Model):
    libro = models.ForeignKey(Libro, related_name="prestamos")
    usuario = models.ForeignKey(settings. AUTH_USER_MODEL, related_name="prestamos")
    fecha_prestamo = models.DateField(default=timezone.now)
    fecha_max = models.DateField()
    fecha_devolucion = models.DateField(blank=True, null=True)

    def __str__(self):
       return f"prestamo de {self.libo} a {self.usuario}"

    @property
    def dias_retraso(self):
         hoy = timezone.now().date()
         fecha_ref = self.fecha_devolucion or hoy
         if fecha_ref > self.fecha_max:
              return(fecha_ref - self.fecha_devolucion).days
         
    @property
    def multa_retraso(self):
         tarifa = 0.50
    def dias_retraso(self):
         return self.dias_retraso * tarifa 

class Multa(models.Model):
     prestamo = models.ForeignKey(Prestamo, related_name="multas")
     tipo = models.CharField(max_length=10, choices=(('r','retraso'), ('p', 'perdida'),('d','deterioro')))
     monto = models.DecimalField(max_digits=3, decimal_places=2, default=0)
     pagada = models.BooleanField(default=False)
     fecha = models.DateField(default=timezone.now)

    def __str__(self):
     return f"Multa {self.tipo} - {self.monto} - {self.prestamo}"
   
    def save(self, *args* **kwargs):