from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import GestorUser

class GestorUserAdmin(UserAdmin):
    model = GestorUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'rol', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = (
        ('Información de Acceso', {
            'fields': ('username', 'password')
        }),
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'email', 'Fecha_nacimiento')
        }),
        ('Rol y Permisos', {
            'fields': ('rol', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Fechas Importantes', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        ('Crear Usuario', {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'Fecha_nacimiento'),
        }),
        ('Rol y Permisos', {
            'fields': ('rol', 'is_staff', 'is_active', 'is_superuser', 'groups'),
        }),
    )

# Registrar el modelo personalizado
admin.site.register(GestorUser, GestorUserAdmin)