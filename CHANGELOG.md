# Changelog — API Gestionnaire de Tâches (JWT)

Toutes les modifications notables apportées à cette API sont documentées dans ce fichier.
Ce projet suit les principes du [Semantic Versioning](https://semver.org/lang/fr/).

---

## [v2.0.0] - 2026-10-28 (Version `v2` — `/api/v2/taches/`)

### Ajouté
- **Gestion de la priorité des tâches** : Ajout du champ `priorite` (`basse`, `moyenne`, `haute`, par défaut `moyenne`) dans le modèle `Tache` et dans le serializer `TacheSerializerV2`.
- **Libellés lisibles** : Ajout des champs en lecture seule `statut_libelle` et `priorite_libelle` dans les réponses de la `v2` pour faciliter l'affichage côté client (Frontend).
- **Documentation OpenAPI / Swagger UI** :
  - Génération dynamique du schéma OpenAPI 3.0 avec `drf-spectacular` (`/api/schema/`).
  - Interface interactive Swagger UI (`/api/docs/`) avec sélecteur de version (`v1` / `v2`).
  - Interface de lecture ReDoc (`/api/redoc/`).

### Corrigé
- Correction de la clé `DEFAULT_AUTHENTICATION_CLASSES` dans `settings.py` pour activer correctement l'authentification JWT avec `SimpleJWT`.
- Correction de la lecture des variables `HOST` et `PORT` depuis le fichier `.env` pour la connexion PostgreSQL.

---

## [v1.0.0] - 2026-10-25 (Version `v1` — `/api/v1/taches/`)

### Ajouté
- **CRUD complet des tâches** :
  - `GET /api/v1/taches/` : Lister toutes les tâches.
  - `POST /api/v1/taches/` : Créer une tâche (`titre`, `description`, `statut`).
  - `GET /api/v1/taches/<id>/` : Consulter le détail d'une tâche.
  - `PUT /api/v1/taches/<id>/` : Remplacer complètement une tâche.
  - `PATCH /api/v1/taches/<id>/` : Modifier partiellement une tâche (ex: changer son statut).
  - `DELETE /api/v1/taches/<id>/` : Supprimer une tâche.
- **Authentification JWT** :
  - `POST /api/token/` : Obtenir un couple de tokens (`access` et `refresh`).
  - `POST /api/token/refresh/` : Rafraîchir le token d'accès.
