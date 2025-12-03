from django.db import models
from django.conf import settings

class Curso(models.Model):
    NIVEL_CHOICES = [
        ('BASICA', 'Educación Básica'),
        ('MEDIA', 'Educación Media'),
        ('SUPERIOR', 'Educación Superior'),
    ]
    
    nombre = models.CharField(max_length=200, verbose_name='Nombre del curso')
    codigo = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name='Código')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    nivel = models.CharField(max_length=10, choices=NIVEL_CHOICES, default='BASICA', blank=True, verbose_name='Nivel')
    ano = models.IntegerField(blank=True, null=True, verbose_name='Año')
    capacidad_maxima = models.IntegerField(default=30, blank=True, verbose_name='Capacidad máxima')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='cursos_creados',
        verbose_name='Creado por'
    )
    
    class Meta:
        ordering = ['nombre']
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
    
    def __str__(self):
        if self.codigo:
            return f"{self.nombre} - {self.codigo}"
        return self.nombre
    
    def total_alumnos(self):
        """Retorna el total de alumnos inscritos"""
        return self.alumnos.count()
    
    def tiene_cupos_disponibles(self):
        """Verifica si hay cupos disponibles"""
        return self.total_alumnos() < self.capacidad_maxima


class Alumno(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    apellido = models.CharField(max_length=100, verbose_name='Apellido')
    rut = models.CharField(max_length=12, unique=True, verbose_name='RUT')
    email = models.EmailField(blank=True, null=True, verbose_name='Correo electrónico')
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name='Teléfono')
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento')
    curso = models.ForeignKey(
        'Curso', 
        on_delete=models.CASCADE, 
        related_name='alumnos',
        verbose_name='Curso'
    )
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='alumnos_creados',
        verbose_name='Creado por'
    )
    
    class Meta:
        ordering = ['apellido', 'nombre']
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    def nombre_completo(self):
        """Retorna el nombre completo del alumno"""
        return f"{self.nombre} {self.apellido}"
    
@property
def edad(self):
    """Calcula la edad del alumno"""
    from datetime import date
    today = date.today()
    edad = today.year - self.fecha_nacimiento.year
    if (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
        edad -= 1
    return edad