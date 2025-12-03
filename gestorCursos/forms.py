from django import forms
from .models import Curso, Alumno

class CursoForm(forms.ModelForm):
    """Formulario para crear/editar cursos"""
    
    class Meta:
        model = Curso
        fields = ['nombre', 'codigo']  # Solo nombre y código
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 1° Medio A'
            }),
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 1MA'
            }),
        }


class AlumnoForm(forms.ModelForm):
    """Formulario para crear/editar alumnos"""
    
    class Meta:
        model = Alumno
        fields = ['nombre', 'apellido', 'rut', 'email', 'telefono', 'fecha_nacimiento', 'curso']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del alumno'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido del alumno'
            }),
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '12345678-9'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56 9 1234 5678'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'curso': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'rut': 'RUT',
            'email': 'Correo Electrónico',
            'telefono': 'Teléfono',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'curso': 'Curso',
        }
    
    def clean_rut(self):
        """Validación personalizada del RUT"""
        rut = self.cleaned_data.get('rut')
        if rut:
            # Aquí puedes agregar validación de RUT chileno
            rut = rut.replace('.', '').replace('-', '').upper()
        return rut