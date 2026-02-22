from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from produits_app.models import Produit

User = get_user_model()

class Commande(models.Model):
    """
    Modèle pour les commandes
    """
    STATUT_CHOICES = (
        ('EN_ATTENTE', 'En attente'),
        ('EN_PREPARATION', 'En préparation'),
        ('PRETE', 'Prête'),
        ('SERVIE', 'Servie'),
        ('ANNULEE', 'Annulée'),
    )
    
    TYPE_CHOICES = (
        ('SUR_PLACE', 'Sur place'),
        ('EMPORTER', 'À emporter'),
        ('LIVRAISON', 'Livraison'),
    )
    
    reference = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Référence'
    )
    client = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Client'
    )
    nom_client = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Nom du client'
    )
    type_commande = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='SUR_PLACE',
        verbose_name='Type de commande'
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='EN_ATTENTE',
        verbose_name='Statut'
    )
    montant_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Montant total'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Notes'
    )
    date_commande = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de commande'
    )
    date_mise_a_jour = models.DateTimeField(
        auto_now=True,
        verbose_name='Date de mise à jour'
    )
    
    class Meta:
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'
        ordering = ['-date_commande']
    
    def __str__(self):
        return f"Commande {self.reference} - {self.get_statut_display()}"
    
    def save(self, *args, **kwargs):
        if not self.reference:
            # Générer une référence unique
            import uuid
            self.reference = f"CMD{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    @property
    def nombre_articles(self):
        return self.lignes_commande.count()
    
    def calculer_montant_total(self):
        total = sum(ligne.prix_total for ligne in self.lignes_commande.all())
        self.montant_total = total
        self.save()

class LigneCommande(models.Model):
    """
    Modèle pour les lignes de commande
    """
    commande = models.ForeignKey(
        Commande,
        on_delete=models.CASCADE,
        related_name='lignes_commande',
        verbose_name='Commande'
    )
    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE,
        verbose_name='Produit'
    )
    quantite = models.PositiveIntegerField(
        default=1,
        verbose_name='Quantité'
    )
    prix_unitaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Prix unitaire'
    )
    prix_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Prix total'
    )
    
    class Meta:
        verbose_name = 'Ligne de commande'
        verbose_name_plural = 'Lignes de commande'
    
    def __str__(self):
        return f"{self.quantite} x {self.produit.nom}"
    
    def save(self, *args, **kwargs):
        self.prix_total = self.quantite * self.prix_unitaire
        super().save(*args, **kwargs)
        
        # Mettre à jour le montant total de la commande
        self.commande.calculer_montant_total()
