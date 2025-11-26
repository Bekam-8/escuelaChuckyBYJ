from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class GestorUser(AbstractUser):
    ROL_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('NORMAL', 'Usuario Normal'),
    ]

    Fecha_nacimiento = models.DateField(null=True, blank=True)
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default='NORMAL')

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"
