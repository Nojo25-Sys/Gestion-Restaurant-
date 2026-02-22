from django.urls import path
from . import views

app_name = 'commandes_app'

urlpatterns = [
    # Dashboard commandes
    path('', views.dashboard_commandes, name='dashboard'),
    
    # Commandes
    path('commandes/', views.commande_list, name='commande_list'),
    path('commandes/<int:pk>/', views.commande_detail, name='commande_detail'),
    path('commandes/ajouter/', views.commande_create, name='commande_create'),
    path('commandes/<int:pk>/modifier/', views.commande_update, name='commande_update'),
    path('commandes/<int:pk>/supprimer/', views.commande_delete, name='commande_delete'),
    path('commandes/<int:pk>/statut/', views.commande_update_statut, name='commande_update_statut'),
    
    # Lignes de commande
    path('commandes/<int:commande_pk>/ajouter-ligne/', views.ajouter_ligne_commande, name='ajouter_ligne_commande'),
    path('lignes-commande/<int:pk>/supprimer/', views.supprimer_ligne_commande, name='supprimer_ligne_commande'),
]
