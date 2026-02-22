from django.db import models
from django.utils import timezone
from produits_app.models import Produit

class MouvementStock(models.Model):
    """
    Modèle pour les mouvements de stock
    """
    TYPE_CHOICES = (
        ('ENTREE', 'Entrée'),
        ('SORTIE', 'Sortie'),
        ('AJUSTEMENT', 'Ajustement'),
        ('PERTE', 'Perte'),
        ('RETOUR', 'Retour client'),
    )
    
    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE,
        related_name='mouvements',
        verbose_name='Produit'
    )
    type_mouvement = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name='Type de mouvement'
    )
    quantite = models.IntegerField(
        verbose_name='Quantité'
    )
    motif = models.TextField(
        blank=True,
        null=True,
        verbose_name='Motif'
    )
    date_mouvement = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date du mouvement'
    )
    utilisateur = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Utilisateur'
    )
    
    class Meta:
        verbose_name = 'Mouvement de stock'
        verbose_name_plural = 'Mouvements de stock'
        ordering = ['-date_mouvement']
    
    def __str__(self):
        return f"{self.get_type_mouvement_display()} - {self.quantite} x {self.produit.nom}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Mettre à jour le stock du produit
        if self.type_mouvement == 'ENTREE' or self.type_mouvement == 'RETOUR':
            self.produit.stock_actuel += self.quantite
        elif self.type_mouvement == 'SORTIE' or self.type_mouvement == 'PERTE':
            self.produit.stock_actuel -= self.quantite
        elif self.type_mouvement == 'AJUSTEMENT':
            self.produit.stock_actuel = self.quantite
        
        self.produit.save()
