from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import GestorUser
from django.forms import ModelForm

# Formulario MEJORADO para registrar nuevos usuarios
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com'
        })
    )
    
    first_name = forms.CharField(
        required=False,
        label="Nombre",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu nombre'
        })
    )
    
    last_name = forms.CharField(
        required=False,
        label="Apellido",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu apellido'
        })
    )
    
    Fecha_nacimiento = forms.DateField(
        required=False,
        label="Fecha de nacimiento",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    class Meta:
        model = GestorUser
        fields = ['username', 'email', 'first_name', 'last_name', 'Fecha_nacimiento', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'nombre_usuario'
            }),
        }
        labels = {
            'username': 'Nombre de usuario',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar campos de contraseña
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '••••••••'
        })
        self.fields['password1'].label = 'Contraseña'
        
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '••••••••'
        })
        self.fields['password2'].label = 'Confirmar contraseña'
        
        # Mensaje de ayuda personalizado
        self.fields['password1'].help_text = """
        <ul class="list-unstyled small text-muted mt-1">
            <li>• Mínimo 8 caracteres</li>
            <li>• No puede ser completamente numérica</li>
            <li>• No puede ser demasiado común</li>
        </ul>
        """
        
        self.fields['username'].help_text = '<small class="form-text text-muted">150 caracteres o menos. Solo letras, dígitos y @/./+/-/_</small>'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if GestorUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.rol = 'NORMAL'  # Por defecto todos son usuarios normales
        if commit:
            user.save()
        return user


# Formulario para editar perfil de usuario
class UserUpdateForm(ModelForm):
    email = forms.EmailField(
        required=True, 
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    first_name = forms.CharField(
        required=False,
        label="Nombre",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    last_name = forms.CharField(
        required=False,
        label="Apellido",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    Fecha_nacimiento = forms.DateField(
        required=False,
        label="Fecha de nacimiento",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    class Meta:
        model = GestorUser
        fields = ['username', 'email', 'first_name', 'last_name', 'Fecha_nacimiento']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }


# Formulario para login personalizado
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario'
        })
    )
    password = forms.CharField(
        label="Contraseña", 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '••••••••'
        })
    )