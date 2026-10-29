from rest_framework import serializers

from .models import Tache


# Serializer de la version 1 (v1) : retourne uniquement les champs de base d'une tâche
class TacheSerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Tache
        fields = ['id', 'titre', 'description', 'statut', 'date_creation']


# Serializer de la version 2 (v2) : enrichit la réponse avec la priorité et les libellés lisibles
class TacheSerializerV2(serializers.ModelSerializer):
    # Champs en lecture seule pour afficher le texte lisible du statut et de la priorité
    statut_libelle = serializers.CharField(source='get_statut_display', read_only=True)
    priorite_libelle = serializers.CharField(source='get_priorite_display', read_only=True)

    class Meta:
        model = Tache
        fields = [
            'id',
            'titre',
            'description',
            'statut',
            'statut_libelle',
            'priorite',
            'priorite_libelle',
            'date_creation',
        ]
