from django import forms
from .models import Commande, LigneCommande
from produits_app.models import Produit

class CommandeForm(forms.ModelForm):
    """
    Formulaire pour les commandes
    """
    class Meta:
        model = Commande
        fields = ['nom_client', 'type_commande', 'notes']
        widgets = {
            'nom_client': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du client'}),
            'type_commande': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class LigneCommandeForm(forms.ModelForm):
    """
    Formulaire pour les lignes de commande
    """
    class Meta:
        model = LigneCommande
        fields = ['produit', 'quantite']
        widgets = {
            'produit': forms.Select(attrs={'class': 'form-control'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['produit'].queryset = Produit.objects.filter(is_active=True, stock_actuel__gt=0)
