from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Sum
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta

from .models import Commande, LigneCommande
from produits_app.models import Produit
from .forms import CommandeForm, LigneCommandeForm


@login_required
@transaction.atomic
def ajouter_ligne_commande(request, commande_pk):
    commande = get_object_or_404(Commande, pk=commande_pk)

    if request.method == 'POST':
        form = LigneCommandeForm(request.POST)
        if form.is_valid():
            produit_id = form.cleaned_data['produit'].pk
            quantite   = form.cleaned_data['quantite']

            # Verrou pessimiste sur la ligne produit
            try:
                produit = Produit.objects.select_for_update(nowait=True).get(pk=produit_id)
            except Produit.DoesNotExist:
                messages.error(request, 'Produit introuvable.')
                return redirect('commandes_app:commande_detail', pk=commande.pk)

            if produit.stock_actuel < quantite:
                messages.error(request, f'Stock insuffisant pour {produit.nom}. Disponible : {produit.stock_actuel}.')
                return redirect('commandes_app:commande_detail', pk=commande.pk)

            ligne               = form.save(commit=False)
            ligne.commande      = commande
            ligne.prix_unitaire = produit.prix_vente
            ligne.save()

            # Décrémentation atomique directe en base
            Produit.objects.filter(pk=produit_id).update(
                stock_actuel=produit.stock_actuel - quantite
            )
            messages.success(request, 'Produit ajouté à la commande.')
            return redirect('commandes_app:commande_detail', pk=commande.pk)
    else:
        form = LigneCommandeForm()

    return render(request, 'commandes_app/ligne_commande_form.html', {
        'form': form, 'commande': commande, 'title': 'Ajouter un produit',
    })


@login_required
@transaction.atomic
def supprimer_ligne_commande(request, pk):
    ligne       = get_object_or_404(LigneCommande, pk=pk)
    commande_pk = ligne.commande.pk

    if request.method == 'POST':
        produit_id = ligne.produit_id
        quantite   = ligne.quantite

        # Verrou avant remise en stock
        produit = Produit.objects.select_for_update().get(pk=produit_id)
        Produit.objects.filter(pk=produit_id).update(
            stock_actuel=produit.stock_actuel + quantite
        )
        ligne.delete()
        messages.success(request, 'Produit retiré de la commande.')
        return redirect('commandes_app:commande_detail', pk=commande_pk)

    return render(request, 'commandes_app/ligne_commande_delete.html', {'ligne': ligne})


# Les autres vues restent identiques à l'original
@login_required
def commande_list(request):
    commandes = Commande.objects.select_related('client').all()
    statut = request.GET.get('statut')
    query  = request.GET.get('q')
    if statut:
        commandes = commandes.filter(statut=statut)
    if query:
        commandes = commandes.filter(Q(reference__icontains=query) | Q(nom_client__icontains=query))
    page_obj = Paginator(commandes, 20).get_page(request.GET.get('page'))
    return render(request, 'commandes_app/commande_list.html', {
        'page_obj': page_obj, 'commandes': page_obj, 'statut': statut, 'query': query,
    })


@login_required
def commande_detail(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    lignes   = commande.lignes_commande.select_related('produit').all()
    return render(request, 'commandes_app/commande_detail.html', {
        'commande': commande, 'lignes_commande': lignes,
    })


@login_required
def commande_create(request):
    if request.method == 'POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
            commande = form.save()
            messages.success(request, f'Commande {commande.reference} créée.')
            return redirect('commandes_app:commande_detail', pk=commande.pk)
    else:
        form = CommandeForm()
    return render(request, 'commandes_app/commande_form.html', {'form': form, 'title': 'Nouvelle commande'})


@login_required
def commande_update(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    if request.method == 'POST':
        form = CommandeForm(request.POST, instance=commande)
        if form.is_valid():
            form.save()
            messages.success(request, 'Commande mise à jour.')
            return redirect('commandes_app:commande_detail', pk=commande.pk)
    else:
        form = CommandeForm(instance=commande)
    return render(request, 'commandes_app/commande_form.html', {
        'form': form, 'title': 'Modifier la commande', 'commande': commande,
    })


@login_required
def commande_update_statut(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    nouveau_statut = request.POST.get('statut')
    if nouveau_statut in [c[0] for c in Commande.STATUT_CHOICES]:
        commande.statut = nouveau_statut
        commande.save(update_fields=['statut', 'date_mise_a_jour'])
        messages.success(request, f'Statut mis à jour : {commande.get_statut_display()}')
    else:
        messages.error(request, 'Statut invalide.')
    return redirect('commandes_app:commande_detail', pk=pk)


@login_required
def commande_delete(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    if request.method == 'POST':
        commande.delete()
        messages.success(request, 'Commande supprimée.')
        return redirect('commandes_app:commande_list')
    return render(request, 'commandes_app/commande_delete.html', {'commande': commande})


@login_required
def dashboard_commandes(request):
    today = timezone.now().date()
    commandes_today = Commande.objects.filter(date_commande__date=today)
    ca_today = commandes_today.aggregate(total=Sum('montant_total'))['total'] or 0

    dates, par_jour = [], []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        dates.append(d.strftime('%d/%m'))
        par_jour.append(Commande.objects.filter(date_commande__date=d).count())

    return render(request, 'commandes_app/dashboard.html', {
        'chiffre_affaires_today': ca_today,
        'commandes_today':  commandes_today.count(),
        'total_commandes':  Commande.objects.count(),
        'commandes_en_attente': Commande.objects.filter(statut='EN_ATTENTE').count(),
        'commandes_en_cours':   Commande.objects.filter(statut__in=['EN_ATTENTE', 'EN_PREPARATION']).count(),
        'commandes_annulees':   Commande.objects.filter(statut='ANNULEE').count(),
        'commandes_recentes':   Commande.objects.order_by('-date_commande')[:10],
        'dates_graphique':      dates,
        'commandes_graphique':  par_jour,
        'statuts_labels': ['En attente', 'En prépa.', 'Prête', 'Servie', 'Annulée'],
        'statuts_data': [
            Commande.objects.filter(statut=s).count()
            for s in ('EN_ATTENTE', 'EN_PREPARATION', 'PRETE', 'SERVIE', 'ANNULEE')
        ],
    })