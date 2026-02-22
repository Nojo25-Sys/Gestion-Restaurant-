from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, F
from django.core.paginator import Paginator
from .models import MouvementStock
from .forms import MouvementStockForm
from produits_app.models import Produit

@login_required
def dashboard_stock(request):
    """
    Dashboard des stocks
    """
    # Statistiques générales
    total_produits = Produit.objects.count()
    produits_en_stock = Produit.objects.filter(stock_actuel__gt=0).count()
    produits_en_rupture = Produit.objects.filter(stock_actuel=0).count()
    stock_critique = Produit.objects.filter(stock_actuel__lte=F('seuil_alerte')).count()
    
    # Valeur du stock
    valeur_stock = Produit.objects.aggregate(
        total=Sum(F('stock_actuel') * F('prix_vente'))
    )['total'] or 0
    
    # Derniers mouvements
    derniers_mouvements = MouvementStock.objects.select_related('produit').order_by('-date_mouvement')[:10]
    
    # Produits en alerte
    produits_alerte = Produit.objects.filter(
        stock_actuel__lte=F('seuil_alerte'),
        stock_actuel__gt=0
    ).order_by('stock_actuel')[:10]
    
    context = {
        'total_produits': total_produits,
        'produits_en_stock': produits_en_stock,
        'produits_en_rupture': produits_en_rupture,
        'stock_critique': stock_critique,
        'valeur_stock': valeur_stock,
        'derniers_mouvements': derniers_mouvements,
        'produits_alerte': produits_alerte,
    }
    
    return render(request, 'stock_app/dashboard.html', context)

@login_required
def mouvement_list(request):
    """
    Liste des mouvements de stock
    """
    mouvements = MouvementStock.objects.select_related('produit', 'utilisateur').all()
    
    # Filtrage par type
    type_mouvement = request.GET.get('type')
    if type_mouvement:
        mouvements = mouvements.filter(type_mouvement=type_mouvement)
    
    # Filtrage par produit
    produit_id = request.GET.get('produit')
    if produit_id:
        mouvements = mouvements.filter(produit_id=produit_id)
    
    # Pagination
    paginator = Paginator(mouvements, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'stock_app/mouvement_list.html', {
        'page_obj': page_obj,
        'mouvements': page_obj,
        'type_mouvement': type_mouvement,
        'produit_id': produit_id,
    })

@login_required
def mouvement_create(request):
    """
    Création d'un mouvement de stock
    """
    produit_id = request.GET.get('produit_id')
    
    if request.method == 'POST':
        form = MouvementStockForm(request.POST)
        if form.is_valid():
            mouvement = form.save(commit=False)
            mouvement.utilisateur = request.user
            mouvement.save()
            messages.success(request, 'Mouvement de stock enregistré avec succès.')
            return redirect('stock_app:mouvement_list')
    else:
        initial_data = {}
        if produit_id:
            try:
                produit = Produit.objects.get(id=produit_id)
                initial_data['produit'] = produit
            except Produit.DoesNotExist:
                pass
        form = MouvementStockForm(initial=initial_data)
    
    return render(request, 'stock_app/mouvement_form.html', {
        'form': form,
        'title': 'Nouveau mouvement de stock'
    })

@login_required
def stock_alertes(request):
    """
    Page des alertes de stock
    """
    # Produits en rupture
    produits_rupture = Produit.objects.filter(stock_actuel=0).order_by('nom')
    
    # Produits en alerte (stock faible)
    produits_alerte = Produit.objects.filter(
        stock_actuel__gt=0,
        stock_actuel__lte=F('seuil_alerte')
    ).order_by('stock_actuel')
    
    context = {
        'produits_rupture': produits_rupture,
        'produits_alerte': produits_alerte,
    }
    
    return render(request, 'stock_app/stock_alertes.html', context)
