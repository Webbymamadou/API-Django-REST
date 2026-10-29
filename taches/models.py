from django.db import models

# Modèle représentant une tâche dans la base de données
class Tache(models.Model):
    # Liste des états possibles pour le suivi d'une tâche
    STATUT_CHOICES = [
        ('a_faire', 'A faire'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminée')
    ]

    # Niveaux de priorité ajoutés pour enrichir la version v2 de l'API
    PRIORITE_CHOICES = [
        ('basse', 'Basse'),
        ('moyenne', 'Moyenne'),
        ('haute', 'Haute')
    ]

    titre = models.CharField(max_length=50)
    description = models.TextField(max_length=255)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='a_faire')
    priorite = models.CharField(max_length=10, choices=PRIORITE_CHOICES, default='moyenne')
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} - {self.statut}"
