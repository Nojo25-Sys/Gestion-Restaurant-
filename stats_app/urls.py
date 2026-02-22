from django.urls import path
from . import views

app_name = 'stats_app'

urlpatterns = [
    # Dashboard statistiques
    path('', views.dashboard_stats, name='dashboard'),
    
    # Pages détaillées
    path('chiffre-affaires/', views.chiffre_affaires, name='chiffre_affaires'),
    path('export-ca/', views.export_ca, name='export_ca'),
    path('produits/', views.produits_stats, name='produits_stats'),
    path('commandes/', views.commandes_stats, name='commandes_stats'),
]
