from django import forms
from .models import MouvementStock
from produits_app.models import Produit

class MouvementStockForm(forms.ModelForm):
    """
    Formulaire pour les mouvements de stock
    """
    class Meta:
        model = MouvementStock
        fields = ['produit', 'type_mouvement', 'quantite', 'motif']
        widgets = {
            'produit': forms.Select(attrs={'class': 'form-control'}),
            'type_mouvement': forms.Select(attrs={'class': 'form-control'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'motif': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
