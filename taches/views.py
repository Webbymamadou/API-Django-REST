from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tache
from .serializers import TacheSerializerV1, TacheSerializerV2


class TacheAPIView(APIView):
    """
    Vue pour lister toutes les tâches ou en créer une nouvelle.
    Supporte le versioning d'API (v1 et v2).
    """

    # Fonction utilisée par DRF et par drf-spectacular pour choisir le serializer selon la version (v1 ou v2)
    def get_serializer_class(self):
        if getattr(self.request, 'version', 'v1') == 'v2':
            return TacheSerializerV2
        return TacheSerializerV1

    @extend_schema(
        operation_id="taches_list",
        summary="Lister toutes les tâches",
        description="Récupère la liste des tâches. En v2, inclut aussi la priorité et les libellés complets.",
        tags=["Tâches"],
    )
    def get(self, request, *args, **kwargs):
        # On récupère toutes les tâches en base de données
        taches = Tache.objects.all()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(taches, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Créer une nouvelle tâche",
        description="Permet d'ajouter une tâche en base de données (avec gestion de la priorité en v2).",
        tags=["Tâches"],
    )
    def post(self, request, *args, **kwargs):
        # On valide les données reçues avec le serializer de la version courante (v1 ou v2)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class TacheDetailAPIView(APIView):
    """
    Vue pour récupérer, modifier ou supprimer une tâche précise via son identifiant (pk).
    Supporte le versioning d'API (v1 et v2).
    """

    # Choix dynamique du serializer selon la version appelée (v1 ou v2)
    def get_serializer_class(self):
        if getattr(self.request, 'version', 'v1') == 'v2':
            return TacheSerializerV2
        return TacheSerializerV1

    @extend_schema(
        summary="Détail d'une tâche",
        description="Récupère les informations d'une tâche via son ID.",
        tags=["Tâches"],
    )
    def get(self, request, pk, *args, **kwargs):
        # Si la tâche n'existe pas, renvoie automatiquement une erreur 404
        tache = get_object_or_404(Tache, pk=pk)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(tache)
        return Response(serializer.data)

    @extend_schema(
        summary="Modifier partiellement une tâche",
        description="Met à jour uniquement les champs envoyés dans la requête (PATCH).",
        tags=["Tâches"],
    )
    def patch(self, request, pk, *args, **kwargs):
        tache = get_object_or_404(Tache, pk=pk)
        serializer_class = self.get_serializer_class()
        # partial=True permet de ne modifier qu'un seul champ (ex: juste le statut)
        serializer = serializer_class(
            tache,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="Remplacer complètement une tâche",
        description="Met à jour tous les champs obligatoires d'une tâche existante (PUT).",
        tags=["Tâches"],
    )
    def put(self, request, pk, *args, **kwargs):
        tache = get_object_or_404(Tache, pk=pk)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            tache,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="Supprimer une tâche",
        description="Supprime définitivement une tâche de la base de données.",
        responses={204: None},
        tags=["Tâches"],
    )
    def delete(self, request, pk, *args, **kwargs):
        tache = get_object_or_404(Tache, pk=pk)
        tache.delete()
        return Response(status=204)
