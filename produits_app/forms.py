from django import forms
from .models import Categorie, Produit

class CategorieForm(forms.ModelForm):
    """
    Formulaire pour les catégories
    """
    class Meta:
        model = Categorie
        fields = ['nom', 'description']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la catégorie'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description de la catégorie'
            }),
        }

class ProduitForm(forms.ModelForm):
    """
    Formulaire pour les produits
    """
    class Meta:
        model = Produit
        fields = ['nom', 'description', 'categorie', 'prix_vente', 
                  'stock_actuel', 'seuil_alerte', 'unite', 'image', 'is_active']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du produit'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description du produit'
            }),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'prix_vente': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': 'Prix de vente'
            }),
            'stock_actuel': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Stock actuel'
            }),
            'seuil_alerte': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Seuil d\'alerte'
            }),
            'unite': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProduitSearchForm(forms.Form):
    """
    Formulaire de recherche de produits
    """
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher un produit...'
        })
    )
    categorie = forms.ModelChoiceField(
        queryset=Categorie.objects.all(),
        required=False,
        empty_label="Toutes les catégories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    prix_min = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prix min',
            'step': '0.01'
        })
    )
    prix_max = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prix max',
            'step': '0.01'
        })
    )
    en_stock = forms.BooleanField(
        required=False,
        label="En stock uniquement",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
