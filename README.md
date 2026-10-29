# API Authentifiée : Gestionnaire de Tâches avec JWT (Sprint S3 — Ticket T1)

Ce dépôt contient mon travail pour le **Ticket T1 (Documentation Swagger & versioning API)** ainsi que la base du mini-projet de fin de sprint **« API Authentifiée : Gestionnaire de Tâches avec JWT »**.

---

## 1. Synthèse de mes notes de formation (Critère AC1)

### A. Pourquoi documenter une API avec OpenAPI / Swagger ?
- **OpenAPI (anciennement Swagger Specification)** est un standard qui décrit la structure d'une API REST (routes, méthodes HTTP, paramètres, formats JSON attendus en entrée et renvoyés en sortie, codes d'erreur et sécurité JWT) dans un fichier YAML ou JSON.
- **Swagger UI** est l'interface web interactive qui lit ce fichier OpenAPI : elle permet aux développeurs (Frontend, Mobile ou testeurs) de comprendre et de tester directement les endpoints depuis le navigateur (bouton *"Try it out"*) sans avoir besoin de Postman.
- Avec **Django REST Framework (DRF)**, l'outil de référence actuel est **`drf-spectacular`**. Il inspecte automatiquement les `Serializers` et les `Views`, et permet d'enrichir la documentation grâce au décorateur `@extend_schema`.

### B. Pourquoi et comment versionner une API (Versioning v1 / v2) ?
- **Objectif** : Faire évoluer une API (ajouter des champs, modifier une structure de réponse) **sans casser** les applications clientes qui utilisent déjà l'ancienne version (*rétrocompatibilité*).
- **Stratégies de versioning dans DRF** :
  1. `URLPathVersioning` (choisie dans ce projet) : la version est placée directement dans l'URL (`/api/v1/taches/` et `/api/v2/taches/`). C'est la méthode la plus claire et la plus répandue.
  2. `NamespaceVersioning` : similaire mais basée sur les namespaces d'URLs Django.
  3. `AcceptHeaderVersioning` : la version est passée dans le header HTTP `Accept`.
  4. `QueryParameterVersioning` : la version est passée en paramètre (`/api/taches/?version=v1`).
- **Fonctionnement dans le code** : Dans la vue, `request.version` contient `'v1'` ou `'v2'`. La méthode `get_serializer_class()` s'en sert pour retourner soit `TacheSerializerV1` (format simple), soit `TacheSerializerV2` (format enrichi avec la priorité et les libellés).

---

## 2. Lien avec le Mini-Projet S3 et Formuloo Market (Critère AC3)

- **Dans le mini-projet « Gestionnaire de Tâches avec JWT »** :
  - Swagger UI intègre directement le bouton **`Authorize` (Bearer JWT)** : je peux récupérer mon token sur `POST /api/token/`, le coller dans Swagger UI et tester toutes mes routes protégées.
  - Le versioning `v1` / `v2` me permet de garder la structure initiale des tâches en `v1` tout en ajoutant la gestion des priorités (`basse`, `moyenne`, `haute`) et des libellés en `v2`.
- **Dans le projet fil rouge « Formuloo Market »** :
  - L'équipe Frontend pourra consommer la documentation Swagger pour intégrer les endpoints produits/commandes sans attendre d'explications manuelles.
  - Si un endpoint de Formuloo Market doit changer de format à l'avenir, le passage en `v2` évitera de bloquer le reste de l'équipe.

---

## 3. Endpoints disponibles (Critères AC2 & AC4)

### Documentation interactive (Swagger & ReDoc)
| Endpoint | Description |
| :--- | :--- |
| `GET /api/docs/` ou `GET /api/v1/docs/` | **Swagger UI (Version 1 - v1)** |
| `GET /api/v2/docs/` ou `GET /api/docs/?version=v2` | **Swagger UI (Version 2 - v2 avec priorité)** |
| `GET /api/redoc/` | **ReDoc** (documentation lisible) |
| `GET /api/schema/?version=v1` | Téléchargement du schéma OpenAPI 3.0 de la `v1` |
| `GET /api/schema/?version=v2` | Téléchargement du schéma OpenAPI 3.0 de la `v2` |

### Authentification JWT
| Méthode | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/token/` | Connexion : renvoie les tokens `access` et `refresh` |
| `POST` | `/api/token/refresh/` | Rafraîchit le token `access` expiré |

### Gestion des Tâches (Versioning `v1` et `v2`)
* **En `v1` (`/api/v1/taches/`)** : Champs `id`, `titre`, `description`, `statut`, `date_creation`.
* **En `v2` (`/api/v2/taches/`)** : Ajoute `priorite` (`basse`, `moyenne`, `haute`), `statut_libelle` et `priorite_libelle`.

| Méthode | Endpoint (`v1` ou `v2`) | Description |
| :--- | :--- | :--- |
| `GET` | `/api/{version}/taches/` | Lister toutes les tâches |
| `POST` | `/api/{version}/taches/` | Créer une nouvelle tâche |
| `GET` | `/api/{version}/taches/{id}/` | Récupérer une tâche par son ID |
| `PUT` | `/api/{version}/taches/{id}/` | Remplacer complètement une tâche |
| `PATCH` | `/api/{version}/taches/{id}/` | Modifier partiellement une tâche |
| `DELETE` | `/api/{version}/taches/{id}/` | Supprimer une tâche |

---

## 4. Installation et lancement

1. Activer l'environnement virtuel et installer les dépendances :
   ```bash
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Appliquer les migrations PostgreSQL :
   ```bash
   python manage.py migrate
   ```
3. Lancer le serveur de développement :
   ```bash
   python manage.py runserver
   ```
4. Ouvrir Swagger UI dans le navigateur :
   - **http://127.0.0.1:8000/api/docs/**

Consultez également le fichier [CHANGELOG.md](./CHANGELOG.md) pour le détail des évolutions entre la `v1` et la `v2`.
