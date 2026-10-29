from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Interface d'administration Django
    path('admin/', admin.site.urls),

    # Endpoints d'authentification JWT (connexion et rafraîchissement du token)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Génération du schéma OpenAPI (on peut aussi filtrer par version avec ?version=v1 ou ?version=v2)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Interface Swagger UI interactive pour tester les endpoints (et par version /api/v1/docs/ ou /api/v2/docs/)
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url='/api/schema/?version=v1'), name='swagger-ui-v1'),
    path('api/v2/docs/', SpectacularSwaggerView.as_view(url='/api/schema/?version=v2'), name='swagger-ui-v2'),
    # Interface ReDoc pour une lecture claire de la documentation
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Routes de l'API avec gestion du versioning dans l'URL (v1 et v2)
    path('api/<str:version>/', include('taches.urls')),
]
