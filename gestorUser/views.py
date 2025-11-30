from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomLoginForm, UserUpdateForm

# Vista de registro
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registro exitoso.")
            return redirect('perfil')
    else:
        form = CustomUserCreationForm()
    return render(request, 'gestorUser/register.html', {'form': form})

# Vista de login
def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Inicio de sesión exitoso.")
            return redirect('perfil')
    else:
        form = CustomLoginForm()
    return render(request, 'gestorUser/login.html', {'form': form})

# Vista de logout
def logout_view(request):
    logout(request)
    messages.info(request, "Sesión cerrada.")
    return redirect('login')

# Vista de perfil (solo usuarios autenticados)
@login_required
def perfil_view(request):
    return render(request, 'gestorUser/perfil.html', {'user': request.user})

# Vista para editar perfil
@login_required
def editar_perfil_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado.")
            return redirect('perfil')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'gestorUser/editarPerfil.html', {'form': form})