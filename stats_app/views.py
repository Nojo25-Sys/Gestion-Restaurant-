from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Avg, F
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
import csv
from produits_app.models import Produit, Categorie
from commandes_app.models import Commande, LigneCommande
from users.models import User

@login_required
def export_ca(request):
    """
    Exporter les chiffres d'affaires en CSV
    """
    # Récupérer les mêmes filtres que la vue chiffre_affaires
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    periode = request.GET.get('periode')
    
    today = timezone.now().date()
    
    # Définir la période selon les filtres
    if periode == "aujourd'hui":
        date_debut = today
        date_fin = today
    elif periode == 'semaine':
        date_debut = today - timedelta(days=7)
        date_fin = today
    elif periode == 'mois':
        date_debut = today.replace(day=1)
        date_fin = today
    elif periode == 'annee':
        date_debut = today.replace(month=1, day=1)
        date_fin = today
    
    # Filtrer les commandes
    commandes = Commande.objects.filter(statut__in=['PRETE', 'SERVIE'])
    
    if date_debut:
        commandes = commandes.filter(date_commande__date__gte=date_debut)
    if date_fin:
        commandes = commandes.filter(date_commande__date__lte=date_fin)
    
    # Créer la réponse CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="chiffre_affaires_{timezone.now().date()}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Date', 'Référence', 'Client', 'Type', 'Statut', 'Montant Total'])
    
    for commande in commandes.order_by('date_commande'):
        writer.writerow([
            commande.date_commande.strftime('%d/%m/%Y'),
            commande.reference,
            commande.client.get_full_name() if commande.client else commande.nom_client,
            commande.get_type_commande_display(),
            commande.get_statut_display(),
            commande.montant_total
        ])
    
    return response

@login_required
def chiffre_affaires(request):
    """
    Page de chiffre d'affaires détaillé
    """
    today = timezone.now().date()
    
    # Récupérer les filtres
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    periode = request.GET.get('periode')
    
    # Définir la période selon les filtres
    if periode == "aujourd'hui":
        date_debut = today
        date_fin = today
    elif periode == 'semaine':
        date_debut = today - timedelta(days=7)
        date_fin = today
    elif periode == 'mois':
        date_debut = today.replace(day=1)
        date_fin = today
    elif periode == 'annee':
        date_debut = today.replace(month=1, day=1)
        date_fin = today
    
    # Filtrer les commandes
    commandes = Commande.objects.filter(statut__in=['PRETE', 'SERVIE'])
    
    if date_debut:
        commandes = commandes.filter(date_commande__date__gte=date_debut)
    if date_fin:
        commandes = commandes.filter(date_commande__date__lte=date_fin)
    
    # Calculer les statistiques
    chiffre_affaires_total = commandes.aggregate(total=Sum('montant_total'))['total'] or 0
    nombre_commandes = commandes.count()
    panier_moyen = chiffre_affaires_total / nombre_commandes if nombre_commandes > 0 else 0
    nombre_clients = commandes.values('client').distinct().count()
    
    # Statistiques par jour
    statistiques_jour = []
    if date_debut and date_fin:
        delta = date_fin - date_debut
        for i in range(delta.days + 1):
            jour_date = date_debut + timedelta(days=i)
            commandes_jour = commandes.filter(date_commande__date=jour_date)
            
            ca_jour = commandes_jour.aggregate(total=Sum('montant_total'))['total'] or 0
            nb_commandes_jour = commandes_jour.count()
            panier_moyen_jour = ca_jour / nb_commandes_jour if nb_commandes_jour > 0 else 0
            
            # Calculer la progression
            ca_jour_precedent = commandes.filter(date_commande__date=jour_date - timedelta(days=1)).aggregate(total=Sum('montant_total'))['total'] or 0
            progression = ((ca_jour - ca_jour_precedent) / ca_jour_precedent * 100) if ca_jour_precedent > 0 else 0
            
            statistiques_jour.append({
                'date': jour_date,
                'nombre_commandes': nb_commandes_jour,
                'chiffre_affaires': ca_jour,
                'panier_moyen': panier_moyen_jour,
                'progression': progression
            })
    
    # Données pour les graphiques
    dates = [stat['date'].strftime('%d/%m') for stat in statistiques_jour]
    chiffres_affaires = [stat['chiffre_affaires'] for stat in statistiques_jour]
    
    # Répartition par type de commande
    types_stats = commandes.values('type_commande').annotate(
        total=Sum('montant_total')
    ).order_by('-total')
    
    types_labels = [stat['type_commande'].replace('_', ' ').title() for stat in types_stats]
    types_data = [float(stat['total']) for stat in types_stats]
    
    context = {
        'chiffre_affaires_total': chiffre_affaires_total,
        'nombre_commandes': nombre_commandes,
        'panier_moyen': panier_moyen,
        'nombre_clients': nombre_clients,
        'statistiques_jour': statistiques_jour,
        'dates': dates,
        'chiffres_affaires': chiffres_affaires,
        'types_labels': types_labels,
        'types_data': types_data,
    }
    
    return render(request, 'stats_app/chiffre_affaires.html', context)

@login_required
def dashboard_stats(request):
    """
    Dashboard des statistiques
    """
    today = timezone.now().date()
    month_start = today.replace(day=1)
    last_month_start = (month_start - timedelta(days=1)).replace(day=1)
    
    # Chiffre d'affaires
    ca_today = Commande.objects.filter(
        date_commande__date=today,
        statut__in=['PRETE', 'SERVIE']
    ).aggregate(total=Sum('montant_total'))['total'] or 0
    
    ca_month = Commande.objects.filter(
        date_commande__date__gte=month_start,
        statut__in=['PRETE', 'SERVIE']
    ).aggregate(total=Sum('montant_total'))['total'] or 0
    
    ca_last_month = Commande.objects.filter(
        date_commande__date__gte=last_month_start,
        date_commande__date__lt=month_start,
        statut__in=['PRETE', 'SERVIE']
    ).aggregate(total=Sum('montant_total'))['total'] or 0
    
    # Commandes
    commandes_today = Commande.objects.filter(date_commande__date=today).count()
    commandes_month = Commande.objects.filter(date_commande__date__gte=month_start).count()
    
    # Produits
    total_produits = Produit.objects.count()
    produits_actifs = Produit.objects.filter(is_active=True).count()
    produits_en_rupture = Produit.objects.filter(stock_actuel=0).count()
    
    # Catégories
    total_categories = Categorie.objects.count()
    
    # Clients
    total_clients = User.objects.count()
    clients_month = User.objects.filter(date_created__date__gte=month_start).count()
    
    # Top produits vendus
    top_produits = LigneCommande.objects.values('produit__nom').annotate(
        total_vendu=Sum('quantite')
    ).order_by('-total_vendu')[:10]
    
    # Top catégories
    top_categories = LigneCommande.objects.values('produit__categorie__nom').annotate(
        total_vendu=Sum('quantite'),
        total_ca=Sum('prix_total')
    ).order_by('-total_ca')[:10]
    
    # Évolution des commandes (7 derniers jours)
    evolution_data = []
    for i in range(7):
        date = today - timedelta(days=i)
        commandes_jour = Commande.objects.filter(date_commande__date=date).count()
        ca_jour = Commande.objects.filter(
            date_commande__date=date,
            statut__in=['PRETE', 'SERVIE']
        ).aggregate(total=Sum('montant_total'))['total'] or 0
        
        evolution_data.append({
            'date': date.strftime('%d/%m'),
            'commandes': commandes_jour,
            'ca': float(ca_jour)
        })
    
    evolution_data.reverse()
    
    context = {
        'ca_today': ca_today,
        'ca_month': ca_month,
        'ca_last_month': ca_last_month,
        'ca_evolution': ((ca_month - ca_last_month) / ca_last_month * 100) if ca_last_month > 0 else 0,
        'commandes_today': commandes_today,
        'commandes_month': commandes_month,
        'total_produits': total_produits,
        'produits_actifs': produits_actifs,
        'produits_en_rupture': produits_en_rupture,
        'total_categories': total_categories,
        'total_clients': total_clients,
        'clients_month': clients_month,
        'top_produits': top_produits,
        'top_categories': top_categories,
        'evolution_data': evolution_data,
    }
    
    return render(request, 'stats_app/dashboard.html', context)

@login_required
def chiffre_affaires(request):
    """
    Page détaillée du chiffre d'affaires
    """
    today = timezone.now().date()
    month_start = today.replace(day=1)
    
    # CA par mois (12 derniers mois)
    ca_mensuel = []
    for i in range(12):
        month_date = (month_start - timedelta(days=30*i)).replace(day=1)
        month_end = (month_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        ca = Commande.objects.filter(
            date_commande__date__gte=month_date,
            date_commande__date__lte=month_end,
            statut__in=['PRETE', 'SERVIE']
        ).aggregate(total=Sum('montant_total'))['total'] or 0
        
        ca_mensuel.append({
            'month': month_date.strftime('%m/%Y'),
            'ca': float(ca)
        })
    
    ca_mensuel.reverse()
    
    # CA par catégorie
    ca_categories = LigneCommande.objects.values('produit__categorie__nom').annotate(
        total=Sum('prix_total')
    ).order_by('-total')
    
    # CA par type de commande
    ca_types = Commande.objects.values('type_commande').annotate(
        total=Sum('montant_total'),
        count=Count('id')
    ).filter(statut__in=['PRETE', 'SERVIE'])
    
    context = {
        'ca_mensuel': ca_mensuel,
        'ca_categories': ca_categories,
        'ca_types': ca_types,
    }
    
    return render(request, 'stats_app/chiffre_affaires.html', context)

@login_required
def produits_stats(request):
    """
    Statistiques des produits
    """
    # Total des produits
    total_produits = Produit.objects.count()
    
    # Produits les plus vendus
    top_vendus = LigneCommande.objects.values('produit__nom', 'produit__categorie__nom').annotate(
        total_quantite=Sum('quantite'),
        total_ca=Sum('prix_total')
    ).order_by('-total_quantite')[:20]
    
    # Produits les plus rentables
    top_rentables = LigneCommande.objects.values('produit__nom', 'produit__categorie__nom').annotate(
        total_ca=Sum('prix_total')
    ).order_by('-total_ca')[:20]
    
    # État des stocks
    stock_critique = Produit.objects.filter(stock_actuel__lte=F('seuil_alerte')).count()
    stock_rupture = Produit.objects.filter(stock_actuel=0).count()
    
    # Valeur du stock
    valeur_stock = Produit.objects.aggregate(
        valeur=Sum(F('stock_actuel') * F('prix_vente'))
    )['valeur'] or 0
    
    context = {
        'total_produits': total_produits,
        'top_vendus': top_vendus,
        'top_rentables': top_rentables,
        'stock_critique': stock_critique,
        'stock_rupture': stock_rupture,
        'valeur_stock': valeur_stock,
    }
    
    return render(request, 'stats_app/produits.html', context)

@login_required
def commandes_stats(request):
    """
    Statistiques des commandes
    """
    today = timezone.now().date()
    
    # Panier moyen
    panier_moyen = Commande.objects.filter(
        statut__in=['PRETE', 'SERVIE']
    ).aggregate(avg=Avg('montant_total'))['avg'] or 0
    
    # Répartition par statut
    statuts = Commande.objects.values('statut').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Répartition par type
    types = Commande.objects.values('type_commande').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Commandes par jour (30 derniers jours)
    commandes_jour = []
    for i in range(30):
        date = today - timedelta(days=i)
        count = Commande.objects.filter(date_commande__date=date).count()
        commandes_jour.append({
            'date': date.strftime('%d/%m/%Y'),
            'count': count
        })
    
    commandes_jour.reverse()
    
    context = {
        'panier_moyen': panier_moyen,
        'statuts': statuts,
        'types': types,
        'commandes_jour': commandes_jour,
    }
    
    return render(request, 'stats_app/commandes.html', context)
