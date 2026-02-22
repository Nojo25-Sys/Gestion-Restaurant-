from django.urls import path
from . import views

app_name = 'stock_app'

urlpatterns = [
    # Dashboard stock
    path('', views.dashboard_stock, name='dashboard'),
    
    # Mouvements de stock
    path('mouvements/', views.mouvement_list, name='mouvement_list'),
    path('mouvements/ajouter/', views.mouvement_create, name='mouvement_create'),
    
    # Produits en stock faible
    path('alertes/', views.stock_alertes, name='stock_alertes'),
]
