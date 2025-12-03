from django.urls import path
from . import views

urlpatterns = [
    # URLs de Cursos
    path('cursos/', views.lista_cursos, name='lista_cursos'),
    path('cursos/crear/', views.crear_curso, name='crear_curso'),
    path('cursos/<int:pk>/', views.detalle_curso, name='detalle_curso'),
    path('cursos/<int:pk>/editar/', views.editar_curso, name='editar_curso'),
    path('cursos/<int:pk>/eliminar/', views.eliminar_curso, name='eliminar_curso'),
    
    # URLs de Alumnos
    path('alumnos/', views.lista_alumnos, name='lista_alumnos'),
    path('alumnos/crear/', views.crear_alumno, name='crear_alumno'),
    path('alumnos/<int:pk>/', views.detalle_alumno, name='detalle_alumno'),
    path('alumnos/<int:pk>/editar/', views.editar_alumno, name='editar_alumno'),
    path('alumnos/<int:pk>/eliminar/', views.eliminar_alumno, name='eliminar_alumno'),
]