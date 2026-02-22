from django.urls import path
from . import views

app_name = 'produits_app'

urlpatterns = [
    # Accueil produits
    path('', views.home, name='home'),
    
    # Catégories
    path('categories/', views.categorie_list, name='categorie_list'),
    path('categories/ajouter/', views.categorie_create, name='categorie_create'),
    path('categories/<int:pk>/modifier/', views.categorie_update, name='categorie_update'),
    path('categories/<int:pk>/supprimer/', views.categorie_delete, name='categorie_delete'),
    
    # Produits
    path('produits/', views.produit_list, name='produit_list'),
    path('produits/<int:pk>/', views.produit_detail, name='produit_detail'),
    path('produits/ajouter/', views.produit_create, name='produit_create'),
    path('produits/<int:pk>/modifier/', views.produit_update, name='produit_update'),
    path('produits/<int:pk>/supprimer/', views.produit_delete, name='produit_delete'),
]
