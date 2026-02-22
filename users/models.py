from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Modèle utilisateur personnalisé étendant AbstractUser
    """
    ROLE_CHOICES = (
        ('ADMIN', 'Administrateur'),
        ('MANAGER', 'Gestionnaire'),
        ('STAFF', 'Employé'),
        ('CLIENT', 'Client'),
    )
    
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='CLIENT',
        verbose_name='Rôle'
    )
    telephone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        verbose_name='Téléphone'
    )
    adresse = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Adresse'
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Date de mise à jour'
    )
    
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        ordering = ['-date_created']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_admin(self):
        return self.role == 'ADMIN'
    
    @property
    def is_manager(self):
        return self.role in ['ADMIN', 'MANAGER']
    
    @property
    def is_staff_user(self):
        return self.role in ['ADMIN', 'MANAGER', 'STAFF']
