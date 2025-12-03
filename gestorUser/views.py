from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

def index(request):
    """Página principal de la escuela"""
    return render(request, 'gestorUser/index.html')

def login_view(request):
    """Vista de inicio de sesión"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.username}!')
            
            # Redirigir según el tipo de usuario
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'gestorUser/login.html')

def register_view(request):
    """Vista de registro de usuarios MEJORADA"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        from .forms import CustomUserCreationForm
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            # Iniciar sesión automáticamente después del registro
            login(request, user)
            
            messages.success(
                request, 
                f'¡Bienvenido {username}! Tu cuenta ha sido creada exitosamente.'
            )
            return redirect('dashboard')
        else:
            # Mostrar errores específicos
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        from .forms import CustomUserCreationForm
        form = CustomUserCreationForm()
    
    return render(request, 'gestorUser/register.html', {'form': form})

@login_required
def logout_view(request):
    """Vista de cierre de sesión"""
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('index')

@login_required
def dashboard(request):
    """Dashboard principal según el tipo de usuario"""
    if request.user.is_superuser:
        return redirect('dashboard_admin')
    else:
        return redirect('dashboard_usuario')

@login_required
def dashboard_admin(request):
    """Dashboard para administradores"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder al panel de administración.')
        return redirect('dashboard_usuario')
    
    # Estadísticas para el administrador
    from gestorCursos.models import Curso, Alumno
    
    total_cursos = Curso.objects.count()
    total_alumnos = Alumno.objects.count()
    total_usuarios = User.objects.count()
    
    # Cursos recientes
    cursos_recientes = Curso.objects.all().order_by('-fecha_creacion')[:5]
    
    # Alumnos recientes - ✅ CAMBIO AQUÍ
    alumnos_recientes = Alumno.objects.all().order_by('-id')[:5]  # Cambiar -fecha_registro por -id
    
    context = {
        'total_cursos': total_cursos,
        'total_alumnos': total_alumnos,
        'total_usuarios': total_usuarios,
        'cursos_recientes': cursos_recientes,
        'alumnos_recientes': alumnos_recientes,
    }
    
    return render(request, 'gestorUser/dashboard_admin.html', context)

@login_required
def dashboard_usuario(request):
    """Dashboard para usuarios normales"""
    from gestorCursos.models import Curso, Alumno
    
    # Estadísticas del usuario
    total_cursos_disponibles = Curso.objects.count()  # ✅ Todos los cursos
    mis_alumnos = Alumno.objects.filter(creado_por=request.user).count()
    
    # Cursos disponibles (todos, no solo los del usuario)
    cursos_disponibles = Curso.objects.all().order_by('-fecha_creacion')[:5]  # ✅ Todos
    
    # Alumnos del usuario (solo los que él creó)
    alumnos_usuario = Alumno.objects.filter(creado_por=request.user).order_by('-id')[:5]
    
    context = {
        'mis_cursos': total_cursos_disponibles,  # Total de cursos disponibles
        'mis_alumnos': mis_alumnos,  # Solo sus alumnos
        'cursos_usuario': cursos_disponibles,  # Todos los cursos
        'alumnos_usuario': alumnos_usuario,  # Solo sus alumnos
    }
    
    return render(request, 'gestorUser/dashboard_usuario.html', context)
def perfil(request):
    """Vista del perfil del usuario"""
    from gestorCursos.models import Curso, Alumno
    
    mis_cursos = Curso.objects.filter(creado_por=request.user)
    mis_alumnos = Alumno.objects.filter(creado_por=request.user)
    
    context = {
        'mis_cursos': mis_cursos,
        'mis_alumnos': mis_alumnos,
    }
    
    return render(request, 'gestorUser/perfil.html', context)

@login_required
def editar_perfil(request):
    """Vista para editar el perfil del usuario"""
    from gestorCursos.models import Curso, Alumno
    
    if request.method == 'POST':
        # Actualizar datos del usuario
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        messages.success(request, 'Perfil actualizado correctamente.')
        return redirect('perfil')
    
    # Estadísticas del usuario
    mis_cursos = Curso.objects.filter(creado_por=request.user).count()
    mis_alumnos = Alumno.objects.filter(creado_por=request.user).count()
    
    context = {
        'mis_cursos': mis_cursos,
        'mis_alumnos': mis_alumnos,
    }
    
    return render(request, 'gestorUser/editar_perfil.html', context)