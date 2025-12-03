from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Count
from .models import Curso, Alumno
from .forms import CursoForm, AlumnoForm

# Helper function
def es_administrador(user):
    return user.is_superuser

# ==================== VISTAS DE CURSOS ====================

@login_required
def lista_cursos(request):
    """Lista de cursos con estadísticas"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('lista_alumnos')
    
    # Anotar con el conteo de alumnos
    cursos = Curso.objects.annotate(
        num_alumnos=Count('alumnos')
    ).select_related('creado_por')
    
    # Filtros
    nivel = request.GET.get('nivel')
    ano = request.GET.get('ano')
    busqueda = request.GET.get('q')
    
    if nivel:
        cursos = cursos.filter(nivel=nivel)
    if ano:
        cursos = cursos.filter(ano=ano)
    if busqueda:
        cursos = cursos.filter(
            Q(nombre__icontains=busqueda) | 
            Q(codigo__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        )
    
    context = {
        'cursos': cursos,
        'nivel_seleccionado': nivel,
        'ano_seleccionado': ano,
        'busqueda': busqueda,
    }
    
    return render(request, 'gestorCursos/cursos/lista_cursos.html', context)


@login_required
@user_passes_test(es_administrador)
def crear_curso(request):
    """Crear nuevo curso"""
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.creado_por = request.user
            curso.save()
            messages.success(request, f'Curso "{curso.nombre}" creado exitosamente.')
            return redirect('lista_cursos')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CursoForm()
    
    return render(request, 'gestorCursos/cursos/form_curso.html', {
        'form': form,
        'titulo': 'Crear Nuevo Curso',
        'accion': 'Crear'
    })


@login_required
@user_passes_test(es_administrador)
def editar_curso(request, pk):
    """Editar curso existente"""
    curso = get_object_or_404(Curso, pk=pk)
    
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, f'Curso "{curso.nombre}" actualizado exitosamente.')
            return redirect('detalle_curso', pk=curso.pk)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CursoForm(instance=curso)
    
    return render(request, 'gestorCursos/cursos/form_curso.html', {
        'form': form,
        'titulo': f'Editar Curso: {curso.nombre}',
        'accion': 'Actualizar',
        'curso': curso
    })


@login_required
def detalle_curso(request, pk):
    """Ver detalle de un curso con sus alumnos"""
    curso = get_object_or_404(Curso, pk=pk)
    
    # Filtrar alumnos según permisos
    if request.user.is_superuser:
        alumnos = curso.alumnos.all().select_related('creado_por')
    else:
        alumnos = curso.alumnos.filter(creado_por=request.user)
    
    context = {
        'curso': curso,
        'alumnos': alumnos,
        'total_alumnos': alumnos.count(),
        'cupos_disponibles': curso.capacidad_maxima - alumnos.count()
    }
    
    return render(request, 'gestorCursos/cursos/detalle_curso.html', context)


@login_required
@user_passes_test(es_administrador)
def eliminar_curso(request, pk):
    """Eliminar curso"""
    curso = get_object_or_404(Curso, pk=pk)
    total_alumnos = curso.total_alumnos()
    
    if request.method == 'POST':
        nombre_curso = curso.nombre
        curso.delete()
        messages.success(request, f'Curso "{nombre_curso}" eliminado exitosamente.')
        return redirect('lista_cursos')
    
    return render(request, 'gestorCursos/cursos/confirmar_eliminar_curso.html', {
        'curso': curso,
        'total_alumnos': total_alumnos
    })


# ==================== VISTAS DE ALUMNOS ====================

@login_required
def lista_alumnos(request):
    """Lista de alumnos con filtros"""
    if request.user.is_superuser:
        alumnos = Alumno.objects.all()
    else:
        alumnos = Alumno.objects.filter(creado_por=request.user)
    
    alumnos = alumnos.select_related('curso', 'creado_por')
    
    # Filtros
    curso_id = request.GET.get('curso')
    busqueda = request.GET.get('q')
    
    if curso_id:
        alumnos = alumnos.filter(curso_id=curso_id)
    
    if busqueda:
        alumnos = alumnos.filter(
            Q(nombre__icontains=busqueda) |
            Q(apellido__icontains=busqueda) |
            Q(rut__icontains=busqueda) |
            Q(email__icontains=busqueda)
        )
    
    # Obtener cursos para el filtro
    if request.user.is_superuser:
        cursos = Curso.objects.all()
    else:
        cursos = Curso.objects.filter(creado_por=request.user)
    
    context = {
        'alumnos': alumnos,
        'cursos': cursos,
        'curso_seleccionado': curso_id,
        'busqueda': busqueda,
        'total_alumnos': alumnos.count()
    }
    
    return render(request, 'gestorCursos/alumnos/lista_alumnos.html', context)


@login_required
def crear_alumno(request):
    """Crear nuevo alumno"""
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.creado_por = request.user
            alumno.save()
            messages.success(request, f'Alumno {alumno.nombre_completo()} creado exitosamente.')
            return redirect('lista_alumnos')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = AlumnoForm()
    
    return render(request, 'gestorCursos/alumnos/crear_alumno.html', {
        'form': form,
        'titulo': 'Crear Nuevo Alumno'
    })


@login_required
def editar_alumno(request, pk):
    """Editar alumno existente"""
    alumno = get_object_or_404(Alumno, pk=pk)
    
    # Verificar permisos
    if alumno.creado_por != request.user and not request.user.is_superuser:
        messages.error(request, 'No tienes permiso para editar este alumno.')
        return redirect('lista_alumnos')
    
    if request.method == 'POST':
        form = AlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
            messages.success(request, f'Alumno {alumno.nombre_completo()} actualizado exitosamente.')
            return redirect('detalle_alumno', pk=alumno.pk)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = AlumnoForm(instance=alumno)
    
    return render(request, 'gestorCursos/alumnos/editar_alumno.html', {
        'form': form,
        'alumno': alumno,
        'titulo': f'Editar Alumno: {alumno.nombre_completo()}'
    })


@login_required
def detalle_alumno(request, pk):
    """Ver detalle de un alumno"""
    alumno = get_object_or_404(Alumno, pk=pk)
    
    # Verificar permisos
    if alumno.creado_por != request.user and not request.user.is_superuser:
        messages.error(request, 'No tienes permiso para ver este alumno.')
        return redirect('lista_alumnos')
    
    return render(request, 'gestorCursos/alumnos/detalle_alumno.html', {
        'alumno': alumno
    })


@login_required
def eliminar_alumno(request, pk):
    """Eliminar alumno"""
    alumno = get_object_or_404(Alumno, pk=pk)
    
    # Verificar permisos
    if alumno.creado_por != request.user and not request.user.is_superuser:
        messages.error(request, 'No tienes permiso para eliminar este alumno.')
        return redirect('lista_alumnos')
    
    if request.method == 'POST':
        nombre_completo = alumno.nombre_completo()
        alumno.delete()
        messages.success(request, f'Alumno {nombre_completo} eliminado exitosamente.')
        return redirect('lista_alumnos')
    
    return render(request, 'gestorCursos/alumnos/eliminar_alumno.html', {
        'alumno': alumno
    })