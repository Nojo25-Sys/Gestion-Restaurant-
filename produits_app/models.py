from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse

class Categorie(models.Model):
    """
    Modèle pour les catégories de produits
    """
    nom = models.CharField(
        max_length=100, 
        unique=True,
        verbose_name='Nom'
    )
    description = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Description'
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
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
        ordering = ['nom']
    
    def __str__(self):
        return self.nom
    
    def get_absolute_url(self):
        return reverse('produits_app:category_detail', kwargs={'pk': self.pk})

class Produit(models.Model):
    """
    Modèle pour les produits
    """
    UNITE_CHOICES = (
        ('UNITE', 'Unité'),
        ('KG', 'Kilogramme'),
        ('LITRE', 'Litre'),
        ('BOITE', 'Boîte'),
        ('BOUTEILLE', 'Bouteille'),
    )
    
    nom = models.CharField(
        max_length=200,
        verbose_name='Nom'
    )
    description = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Description'
    )
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.CASCADE,
        related_name='produits',
        verbose_name='Catégorie'
    )
    prix_vente = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='Prix de vente'
    )
    stock_actuel = models.IntegerField(
        default=0,
        verbose_name='Stock actuel'
    )
    seuil_alerte = models.IntegerField(
        default=10,
        verbose_name='Seuil d\'alerte'
    )
    unite = models.CharField(
        max_length=20,
        choices=UNITE_CHOICES,
        default='UNITE',
        verbose_name='Unité'
    )
    image = models.ImageField(
        upload_to='produits/',
        blank=True,
        null=True,
        verbose_name='Image'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Actif'
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
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'
        ordering = ['-date_created']
    
    def __str__(self):
        return f"{self.nom} ({self.categorie.nom})"
    
    def get_absolute_url(self):
        return reverse('produits_app:detail', kwargs={'pk': self.pk})
    
    def clean(self):
        """
        Validation du modèle
        """
        errors = {}
        
        if self.prix_vente <= 0:
            errors['prix_vente'] = 'Le prix de vente doit être positif.'
        
        if self.stock_actuel < 0:
            errors['stock_actuel'] = 'Le stock ne peut pas être négatif.'
        
        if self.seuil_alerte < 0:
            errors['seuil_alerte'] = 'Le seuil d\'alerte ne peut pas être négatif.'
        
        if errors:
            raise ValidationError(errors)
    
    @property
    def stock_faible(self):
        """
        Vérifie si le stock est bas
        """
        return self.stock_actuel <= self.seuil_alerte
    
    @property
    def en_rupture(self):
        """
        Vérifie si le produit est en rupture
        """
        return self.stock_actuel == 0
