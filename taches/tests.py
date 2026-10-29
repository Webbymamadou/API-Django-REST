from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Tache


class TacheAPITestCase(TestCase):
#Tests des endpoints de gestion des tâches en V1 et V2.

    def setUp(self):
        self.client = APIClient()

        # Les URL correspondent aux routes définies dans config/urls.py
        self.url_liste_v1 = "/api/v1/taches/"
        self.url_liste_v2 = "/api/v2/taches/"

        self.tache1 = Tache.objects.create(
            titre="Apprendre Django",
            description="Comprendre Django REST Framework",
            statut="a_faire",
            priorite="moyenne",
        )

        self.tache2 = Tache.objects.create(
            titre="Apprendre GitHub Actions",
            description="Automatiser les tests",
            statut="en_cours",
            priorite="haute",
        )

    def test_lister_les_taches_v1(self):
        """Vérifie que la V1 retourne les tâches sans le champ priorité."""

        response = self.client.get(self.url_liste_v1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertIn("titre", response.data[0])
        self.assertIn("description", response.data[0])
        self.assertNotIn("priorite", response.data[0])

    def test_lister_les_taches_v2(self):
        """Vérifie que la V2 expose la priorité et ses libellés."""

        response = self.client.get(self.url_liste_v2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        premiere_tache = response.data[0]

        self.assertIn("priorite", premiere_tache)
        self.assertIn("priorite_libelle", premiere_tache)
        self.assertIn("statut_libelle", premiere_tache)

    def test_creer_une_tache_v1(self):
        """Vérifie qu'une requête POST valide crée une tâche en V1."""

        donnees = {
            "titre": "Préparer le pipeline CI/CD",
            "description": "Configurer GitHub Actions",
            "statut": "a_faire",
        }

        nombre_initial = Tache.objects.count()

        response = self.client.post(
            self.url_liste_v1,
            donnees,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tache.objects.count(), nombre_initial + 1)

        self.assertTrue(
            Tache.objects.filter(
                titre="Préparer le pipeline CI/CD"
            ).exists()
        )

    def test_creer_une_tache_v2_avec_priorite(self):
        """Vérifie qu'une tâche peut être créée avec une priorité en V2."""

        donnees = {
            "titre": "Déployer l'API",
            "description": "Préparer le déploiement automatique",
            "statut": "a_faire",
            "priorite": "haute",
        }

        response = self.client.post(
            self.url_liste_v2,
            donnees,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        tache = Tache.objects.get(titre="Déployer l'API")
        self.assertEqual(tache.priorite, "haute")

    def test_refuser_un_titre_trop_long(self):
        """Vérifie qu'un titre de plus de 50 caractères est refusé."""

        donnees = {
            "titre": "A" * 51,
            "description": "Description de la tâche",
            "statut": "a_faire",
        }

        nombre_initial = Tache.objects.count()

        response = self.client.post(
            self.url_liste_v1,
            donnees,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertEqual(Tache.objects.count(), nombre_initial)

    def test_refuser_un_statut_invalide(self):
        """Vérifie qu'un statut absent des choix autorisés est refusé."""

        donnees = {
            "titre": "Tâche invalide",
            "description": "Tester la validation",
            "statut": "inconnu",
        }

        response = self.client.post(
            self.url_liste_v1,
            donnees,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_consulter_une_tache_existante(self):
        """Vérifie la consultation d'une tâche existante."""

        url_detail = f"{self.url_liste_v1}{self.tache1.pk}/"

        response = self.client.get(url_detail)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["titre"], "Apprendre Django")

    def test_consulter_une_tache_inexistante(self):
        """Vérifie qu'une tâche inexistante retourne une erreur 404."""

        url_detail = f"{self.url_liste_v1}999999/"

        response = self.client.get(url_detail)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_modifier_partiellement_une_tache(self):
        """Vérifie que PATCH modifie uniquement les champs transmis."""

        url_detail = f"{self.url_liste_v1}{self.tache1.pk}/"

        response = self.client.patch(
            url_detail,
            {"statut": "en_cours"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.tache1.refresh_from_db()

        self.assertEqual(self.tache1.statut, "en_cours")
        self.assertEqual(self.tache1.titre, "Apprendre Django")

    def test_remplacer_completement_une_tache(self):
        """Vérifie que PUT remplace les champs obligatoires."""

        url_detail = f"{self.url_liste_v1}{self.tache1.pk}/"

        donnees = {
            "titre": "Nouveau titre",
            "description": "Nouvelle description",
            "statut": "termine",
        }

        response = self.client.put(
            url_detail,
            donnees,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.tache1.refresh_from_db()

        self.assertEqual(self.tache1.titre, "Nouveau titre")
        self.assertEqual(self.tache1.description, "Nouvelle description")
        self.assertEqual(self.tache1.statut, "termine")

    def test_supprimer_une_tache(self):
        """Vérifie qu'une tâche existante peut être supprimée."""

        url_detail = f"{self.url_liste_v1}{self.tache1.pk}/"
        nombre_initial = Tache.objects.count()

        response = self.client.delete(url_detail)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertEqual(Tache.objects.count(), nombre_initial - 1)

        self.assertFalse(
            Tache.objects.filter(pk=self.tache1.pk).exists()
        )

    def test_supprimer_une_tache_inexistante(self):
        """Vérifie que la suppression d'une tâche inexistante retourne 404."""

        url_detail = f"{self.url_liste_v1}999999/"

        response = self.client.delete(url_detail)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
