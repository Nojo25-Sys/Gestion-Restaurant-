from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, F
from django.core.paginator import Paginator
from .models import Categorie, Produit
from .forms import CategorieForm, ProduitForm, ProduitSearchForm

def home(request):
    """
    Page d'accueil des produits
    """
    form = ProduitSearchForm(request.GET or None)
    produits = Produit.objects.filter(is_active=True)
    
    # Filtrage
    if form.is_valid():
        if form.cleaned_data.get('query'):
            produits = produits.filter(
                Q(nom__icontains=form.cleaned_data['query']) |
                Q(description__icontains=form.cleaned_data['query'])
            )
        
        if form.cleaned_data.get('categorie'):
            produits = produits.filter(categorie=form.cleaned_data['categorie'])
        
        if form.cleaned_data.get('prix_min'):
            produits = produits.filter(prix_vente__gte=form.cleaned_data['prix_min'])
        
        if form.cleaned_data.get('prix_max'):
            produits = produits.filter(prix_vente__lte=form.cleaned_data['prix_max'])
        
        if form.cleaned_data.get('en_stock'):
            produits = produits.filter(stock_actuel__gt=0)
    
    # Pagination
    paginator = Paginator(produits, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'produits_app/home.html', {
        'form': form,
        'page_obj': page_obj,
        'produits': page_obj,
    })

@login_required
def categorie_list(request):
    """
    Liste des catégories (réservé aux staff)
    """
    if not request.user.is_staff_user:
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    categories = Categorie.objects.all()
    return render(request, 'produits_app/categorie_list.html', {'categories': categories})

@login_required
def categorie_create(request):
    """
    Création d'une catégorie
    """
    if not request.user.is_manager:
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CategorieForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catégorie créée avec succès.')
            return redirect('produits_app:categorie_list')
    else:
        form = CategorieForm()
    
    return render(request, 'produits_app/categorie_form.html', {
        'form': form,
        'title': 'Ajouter une catégorie'
    })

@login_required
def categorie_update(request, pk):
    """
    Mise à jour d'une catégorie
    """
    if not request.user.is_manager:
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    categorie = get_object_or_404(Categorie, pk=pk)
    
    if request.method == 'POST':
        form = CategorieForm(request.POST, instance=categorie)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catégorie mise à jour avec succès.')
            return redirect('produits_app:categorie_list')
    else:
        form = CategorieForm(instance=categorie)
    
    return render(request, 'produits_app/categorie_form.html', {
        'form': form,
        'title': 'Modifier une catégorie',
        'categorie': categorie
    })

@login_required
def categorie_delete(request, pk):
    """
    Suppression d'une catégorie
    """
    if not request.user.is_admin:
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    categorie = get_object_or_404(Categorie, pk=pk)
    
    if categorie.produits.exists():
        messages.error(request, 'Impossible de supprimer cette catégorie car elle contient des produits.')
        return redirect('produits_app:categorie_list')
    
    if request.method == 'POST':
        categorie.delete()
        messages.success(request, 'Catégorie supprimée avec succès.')
        return redirect('produits_app:categorie_list')
    
    return render(request, 'produits_app/categorie_delete.html', {'categorie': categorie})

@login_required
def produit_list(request):
    """
    Liste des produits (réservé au staff)
    """
    if not request.user.is_manager:
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    produits = Produit.objects.all()
    return render(request, 'produits_app/produit_list.html', {'produits': produits})

@login_required
def produit_detail(request, pk):
    """
    Détail d'un produit
    """
    produit = get_object_or_404(Produit, pk=pk)
    return render(request, 'produits_app/produit_detail.html', {'produit': produit})

@login_required
def produit_create(request):
    """
    Création d'un produit
    """
    if not request.user.is_manager:
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produit créé avec succès.')
            return redirect('produits_app:home')
    else:
        form = ProduitForm()
    
    return render(request, 'produits_app/produit_form.html', {
        'form': form,
        'title': 'Ajouter un produit'
    })

@login_required
def produit_update(request, pk):
    """
    Mise à jour d'un produit
    """
    if not request.user.is_manager:
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    produit = get_object_or_404(Produit, pk=pk)
    
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produit mis à jour avec succès.')
            return redirect('produits_app:home')
    else:
        form = ProduitForm(instance=produit)
    
    return render(request, 'produits_app/produit_form.html', {
        'form': form,
        'title': 'Modifier un produit',
        'produit': produit
    })

@login_required
def produit_delete(request, pk):
    """
    Suppression d'un produit
    """
    if not request.user.is_admin:
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    produit = get_object_or_404(Produit, pk=pk)
    
    if request.method == 'POST':
        produit.delete()
        messages.success(request, 'Produit supprimé avec succès.')
        return redirect('produits_app:produit_list')
    
    return render(request, 'produits_app/produit_delete.html', {'produit': produit})
