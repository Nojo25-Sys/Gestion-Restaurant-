from commandes_app.models import Commande, LigneCommande
from produits_app.models import Produit
from users.models import User
from django.utils import timezone

# Récupérer ou créer des données de test
print("Création de données de test pour les commandes...")

# Créer un client test si nécessaire
client, created = User.objects.get_or_create(
    username='client_test',
    defaults={
        'email': 'client@test.com',
        'first_name': 'Client',
        'last_name': 'Test',
        'role': 'CLIENT'
    }
)
if created:
    client.set_password('password123')
    client.save()
    print(f"✅ Client créé: {client.username}")

# Récupérer quelques produits
produits = Produit.objects.all()[:5]
if produits.count() < 3:
    print("❌ Pas assez de produits dans la base de données")
    print("Veuillez d'abord créer des produits avec le script de produits")
else:
    print(f"✅ {produits.count()} produits trouvés")

# Créer quelques commandes
for i in range(3):
    commande = Commande.objects.create(
        client=client,
        nom_client=f"Client Test {i+1}",
        type_commande='SUR_PLACE',
        statut='EN_ATTENTE',
        notes=f"Commande test numéro {i+1}"
    )
    print(f"✅ Commande créée: {commande.reference}")
    
    # Ajouter des produits à la commande
    for j, produit in enumerate(produits[:3]):
        quantite = (j + 1) * 2
        prix_unitaire = produit.prix
        
        ligne = LigneCommande.objects.create(
            commande=commande,
            produit=produit,
            quantite=quantite,
            prix_unitaire=prix_unitaire
        )
        print(f"  - Ajouté: {quantite} x {produit.nom} ({ligne.prix_total} FCFA)")

# Mettre à jour les montants totaux
for commande in Commande.objects.all():
    commande.calculer_montant_total()
    print(f"✅ Montant total de {commande.reference}: {commande.montant_total} FCFA")

print("\n🎉 Données de test créées avec succès!")
print(f"Total commandes: {Commande.objects.count()}")
print(f"Total lignes de commande: {LigneCommande.objects.count()}")
