from django.contrib import admin
from .models import Curso, Alumno

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'nivel', 'ano', 'total_alumnos', 'capacidad_maxima', 'creado_por', 'fecha_creacion')
    list_filter = ('nivel', 'ano', 'creado_por', 'fecha_creacion')
    search_fields = ('nombre', 'codigo', 'descripcion')
    readonly_fields = ('fecha_creacion', 'total_alumnos')
    date_hierarchy = 'fecha_creacion'
    list_per_page = 20
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'codigo', 'descripcion')
        }),
        ('Configuración Académica', {
            'fields': ('nivel', 'ano', 'capacidad_maxima')
        }),
        ('Estadísticas', {
            'fields': ('total_alumnos',),
            'classes': ('collapse',)
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'creado_por'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Solo al crear
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)
    
    def total_alumnos(self, obj):
        return obj.total_alumnos()
    total_alumnos.short_description = 'Total Alumnos'


@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'rut', 'email', 'telefono', 'curso', 'creado_por')
    list_filter = ('curso', 'creado_por', 'fecha_nacimiento')
    search_fields = ('nombre', 'apellido', 'rut', 'email')
    readonly_fields = ()
    date_hierarchy = 'fecha_nacimiento'
    list_per_page = 25
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido', 'rut', 'fecha_nacimiento')
        }),
        ('Información de Contacto', {
            'fields': ('email', 'telefono')
        }),
        ('Información Académica', {
            'fields': ('curso',)
        }),
        ('Metadatos', {
            'fields': ('creado_por',),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Solo al crear
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)
    
    def nombre_completo(self, obj):
        return obj.nombre_completo()
    nombre_completo.short_description = 'Nombre Completo'
    nombre_completo.admin_order_field = 'apellido'