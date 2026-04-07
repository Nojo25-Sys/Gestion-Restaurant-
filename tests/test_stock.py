from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ValidationError
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.contrib.auth import get_user_model
from produits_app.models import Categorie, Produit
from stock_app.models import MouvementStock

User = get_user_model()


class MouvementStockTestCase(TestCase):
    def setUp(self):
        self.user      = User.objects.create_user(username='test', password='test123', role='STAFF')
        self.categorie = Categorie.objects.create(nom='Boissons')
        self.produit   = Produit.objects.create(
            nom='Coca-Cola', categorie=self.categorie,
            prix_vente=1500, stock_actuel=50, seuil_alerte=5,
        )

    def _mvt(self, type_mvt, quantite):
        return MouvementStock.objects.create(
            produit=self.produit, type_mouvement=type_mvt,
            quantite=quantite, utilisateur=self.user,
        )

    def test_entree_incremente(self):
        self._mvt('ENTREE', 10)
        self.produit.refresh_from_db()
        self.assertEqual(self.produit.stock_actuel, 60)

    def test_sortie_decremente(self):
        self._mvt('SORTIE', 20)
        self.produit.refresh_from_db()
        self.assertEqual(self.produit.stock_actuel, 30)

    def test_ajustement_fixe(self):
        self._mvt('AJUSTEMENT', 100)
        self.produit.refresh_from_db()
        self.assertEqual(self.produit.stock_actuel, 100)

    def test_retour_incremente(self):
        self._mvt('RETOUR', 3)
        self.produit.refresh_from_db()
        self.assertEqual(self.produit.stock_actuel, 53)

    def test_stock_insuffisant_leve_erreur(self):
        with self.assertRaises(ValidationError):
            self._mvt('SORTIE', 200)

    def test_quantite_zero_leve_erreur(self):
        m = MouvementStock(produit=self.produit, type_mouvement='ENTREE', quantite=0)
        with self.assertRaises(ValidationError):
            m.clean()

    def test_stock_faible_property(self):
        self.produit.stock_actuel = 5
        self.produit.seuil_alerte = 5
        self.produit.save()
        self.assertTrue(self.produit.stock_faible)

    def test_en_rupture_property(self):
        self.produit.stock_actuel = 0
        self.produit.save()
        self.assertTrue(self.produit.en_rupture)


class ConcurrenceTestCase(TransactionTestCase):
    def setUp(self):
        self.user      = User.objects.create_user(username='concurrent', password='test', role='STAFF')
        self.categorie = Categorie.objects.create(nom='Test')
        self.produit   = Produit.objects.create(
            nom='Produit concurrent', categorie=self.categorie,
            prix_vente=1000, stock_actuel=10, seuil_alerte=1,
        )

    def _sortie(self, quantite):
        try:
            MouvementStock.objects.create(
                produit=self.produit, type_mouvement='SORTIE',
                quantite=quantite, utilisateur=self.user,
            )
            return 'ok'
        except Exception as e:
            return f'erreur:{e}'

    def test_pas_de_stock_negatif(self):
        # 5 threads tentent chacun de sortir 3 unités (total 15 > stock 10)
        with ThreadPoolExecutor(max_workers=5) as ex:
            resultats = [f.result() for f in as_completed([ex.submit(self._sortie, 3) for _ in range(5)])]

        self.produit.refresh_from_db()
        self.assertGreaterEqual(self.produit.stock_actuel, 0)
        self.assertLessEqual(resultats.count('ok'), 3)