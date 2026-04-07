from django.db import models, transaction
from django.core.exceptions import ValidationError


class MouvementStock(models.Model):
    TYPE_CHOICES = (
        ('ENTREE',     'Entrée'),
        ('SORTIE',     'Sortie'),
        ('AJUSTEMENT', 'Ajustement'),
        ('PERTE',      'Perte'),
        ('RETOUR',     'Retour client'),
    )

    produit        = models.ForeignKey('produits_app.Produit', on_delete=models.CASCADE, related_name='mouvements')
    type_mouvement = models.CharField(max_length=20, choices=TYPE_CHOICES)
    quantite       = models.IntegerField()
    motif          = models.TextField(blank=True, null=True)
    date_mouvement = models.DateTimeField(auto_now_add=True)
    utilisateur    = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Mouvement de stock'
        ordering     = ['-date_mouvement']

    def __str__(self):
        return f'{self.get_type_mouvement_display()} — {self.quantite} × {self.produit.nom}'

    def clean(self):
        if self.quantite == 0:
            raise ValidationError({'quantite': 'La quantité ne peut pas être zéro.'})

    @transaction.atomic
    def save(self, *args, **kwargs):
        from produits_app.models import Produit

        # Verrou pessimiste — empêche la race condition
        produit = Produit.objects.select_for_update().get(pk=self.produit_id)

        nouveau_stock = self._calculer_nouveau_stock(produit.stock_actuel)

        if nouveau_stock < 0:
            raise ValidationError(
                f'Stock insuffisant. Actuel : {produit.stock_actuel}, demandé : {self.quantite}.'
            )

        super().save(*args, **kwargs)
        Produit.objects.filter(pk=self.produit_id).update(stock_actuel=nouveau_stock)
        self.produit.stock_actuel = nouveau_stock

    def _calculer_nouveau_stock(self, stock_actuel: int) -> int:
        t = self.type_mouvement
        if t in ('ENTREE', 'RETOUR'):
            return stock_actuel + abs(self.quantite)
        if t in ('SORTIE', 'PERTE'):
            return stock_actuel - abs(self.quantite)
        if t == 'AJUSTEMENT':
            return self.quantite
        return stock_actuel