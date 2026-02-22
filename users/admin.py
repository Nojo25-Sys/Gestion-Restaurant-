from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Configuration de l'admin pour le modèle User personnalisé
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_created')
    list_filter = ('role', 'is_active', 'date_created')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_created',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email')}),
        ('Rôle et contact', {'fields': ('role', 'telephone', 'adresse')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'role', 'telephone', 'adresse', 'password1', 'password2'),
        }),
    )
