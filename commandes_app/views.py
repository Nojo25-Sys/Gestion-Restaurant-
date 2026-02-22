from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from .models import Commande, LigneCommande
from produits_app.models import Produit
from .forms import CommandeForm, LigneCommandeForm

@login_required
def commande_list(request):
    """
    Liste des commandes
    """
    commandes = Commande.objects.all()
    
    # Filtrage par statut
    statut = request.GET.get('statut')
    if statut:
        commandes = commandes.filter(statut=statut)
    
    # Recherche
    query = request.GET.get('q')
    if query:
        commandes = commandes.filter(
            Q(reference__icontains=query) |
            Q(nom_client__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(commandes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'commandes_app/commande_list.html', {
        'page_obj': page_obj,
        'commandes': page_obj,
        'statut': statut,
        'query': query
    })

@login_required
def commande_detail(request, pk):
    """
    Détail d'une commande
    """
    commande = get_object_or_404(Commande, pk=pk)
    lignes_commande = commande.lignes_commande.select_related('produit').all()
    return render(request, 'commandes_app/commande_detail.html', {
        'commande': commande,
        'lignes_commande': lignes_commande
    })

@login_required
def commande_create(request):
    """
    Création d'une commande
    """
    if request.method == 'POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
            commande = form.save()
            messages.success(request, f'Commande {commande.reference} créée avec succès.')
            return redirect('commandes_app:commande_detail', pk=commande.pk)
    else:
        form = CommandeForm()
    
    return render(request, 'commandes_app/commande_form.html', {
        'form': form,
        'title': 'Nouvelle commande'
    })

@login_required
def commande_update(request, pk):
    """
    Mise à jour d'une commande
    """
    commande = get_object_or_404(Commande, pk=pk)
    
    if request.method == 'POST':
        form = CommandeForm(request.POST, instance=commande)
        if form.is_valid():
            form.save()
            messages.success(request, 'Commande mise à jour avec succès.')
            return redirect('commandes_app:commande_detail', pk=commande.pk)
    else:
        form = CommandeForm(instance=commande)
    
    return render(request, 'commandes_app/commande_form.html', {
        'form': form,
        'title': 'Modifier la commande',
        'commande': commande
    })

@login_required
def commande_update_statut(request, pk):
    """
    Mise à jour du statut d'une commande
    """
    commande = get_object_or_404(Commande, pk=pk)
    nouveau_statut = request.POST.get('statut')
    
    if nouveau_statut in [choice[0] for choice in Commande.STATUT_CHOICES]:
        commande.statut = nouveau_statut
        commande.save()
        messages.success(request, f'Statut de la commande mis à jour: {commande.get_statut_display()}')
    else:
        messages.error(request, 'Statut invalide.')
    
    return redirect('commandes_app:commande_detail', pk=pk)

@login_required
def commande_delete(request, pk):
    """
    Suppression d'une commande
    """
    commande = get_object_or_404(Commande, pk=pk)
    
    if request.method == 'POST':
        commande.delete()
        messages.success(request, 'Commande supprimée avec succès.')
        return redirect('commandes_app:commande_list')
    
    return render(request, 'commandes_app/commande_delete.html', {'commande': commande})

@login_required
def ajouter_ligne_commande(request, commande_pk):
    """
    Ajouter une ligne à une commande
    """
    commande = get_object_or_404(Commande, pk=commande_pk)
    
    if request.method == 'POST':
        form = LigneCommandeForm(request.POST)
        if form.is_valid():
            ligne = form.save(commit=False)
            ligne.commande = commande
            ligne.prix_unitaire = ligne.produit.prix_vente
            ligne.save()
            
            # Mettre à jour le stock du produit
            ligne.produit.stock_actuel -= ligne.quantite
            ligne.produit.save()
            
            messages.success(request, 'Produit ajouté à la commande.')
            return redirect('commandes_app:commande_detail', pk=commande.pk)
    else:
        form = LigneCommandeForm()
    
    return render(request, 'commandes_app/ligne_commande_form.html', {
        'form': form,
        'commande': commande,
        'title': 'Ajouter un produit'
    })

@login_required
def supprimer_ligne_commande(request, pk):
    """
    Supprimer une ligne de commande
    """
    ligne = get_object_or_404(LigneCommande, pk=pk)
    commande_pk = ligne.commande.pk
    
    if request.method == 'POST':
        # Remettre le produit en stock
        ligne.produit.stock_actuel += ligne.quantite
        ligne.produit.save()
        
        ligne.delete()
        messages.success(request, 'Produit retiré de la commande.')
        return redirect('commandes_app:commande_detail', pk=commande_pk)
    
    return render(request, 'commandes_app/ligne_commande_delete.html', {'ligne': ligne})

@login_required
def dashboard_commandes(request):
    """
    Dashboard des commandes
    """
    today = timezone.now().date()
    
    # Statistiques du jour
    commandes_today = Commande.objects.filter(date_commande__date=today)
    chiffre_affaires_today = commandes_today.aggregate(
        total=Sum('montant_total')
    )['total'] or 0
    
    # Statistiques générales
    total_commandes = Commande.objects.count()
    commandes_en_attente = Commande.objects.filter(statut='EN_ATTENTE').count()
    commandes_en_cours = Commande.objects.filter(statut__in=['EN_ATTENTE', 'EN_PREPARATION']).count()
    commandes_annulees = Commande.objects.filter(statut='ANNULEE').count()
    
    # Dernières commandes
    commandes_recentes = Commande.objects.order_by('-date_commande')[:10]
    
    # Données pour les graphiques (7 derniers jours)
    from datetime import timedelta
    dates = []
    commandes_par_jour = []
    
    for i in range(7):
        date = today - timedelta(days=i)
        dates.append(date.strftime('%d/%m'))
        nb_commandes = Commande.objects.filter(date_commande__date=date).count()
        commandes_par_jour.append(nb_commandes)
    
    dates.reverse()
    commandes_par_jour.reverse()
    
    # Répartition par statut
    statuts_labels = ['En attente', 'En préparation', 'Prête', 'Servie', 'Annulée']
    statuts_data = [
        Commande.objects.filter(statut='EN_ATTENTE').count(),
        Commande.objects.filter(statut='EN_PREPARATION').count(),
        Commande.objects.filter(statut='PRETE').count(),
        Commande.objects.filter(statut='SERVIE').count(),
        Commande.objects.filter(statut='ANNULEE').count(),
    ]
    
    context = {
        'chiffre_affaires_today': chiffre_affaires_today,
        'commandes_today': commandes_today.count(),
        'total_commandes': total_commandes,
        'commandes_en_attente': commandes_en_attente,
        'commandes_en_cours': commandes_en_cours,
        'commandes_annulees': commandes_annulees,
        'commandes_recentes': commandes_recentes,
        'dates_graphique': dates,
        'commandes_graphique': commandes_par_jour,
        'statuts_labels': statuts_labels,
        'statuts_data': statuts_data,
    }
    
    return render(request, 'commandes_app/dashboard.html', context)
