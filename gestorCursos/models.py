from django.db import models

class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    codigo = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()   

    # Relación con Curso (muchos alumnos pueden pertenecer a un curso)
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name='alumnos'
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
