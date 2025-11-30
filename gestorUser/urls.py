from django.contrib import admin
from django.urls import path, include   # ✅ include se importa aquí
from . import views                     # ✅ tus vistas del proyecto principal

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Página principal
    path('usuarios/', include('gestorUser.urls')),   # Rutas de usuarios
    path('cursos/', include('gestorCursos.urls')),   # Rutas de cursos
]