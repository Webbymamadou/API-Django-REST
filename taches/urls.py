from django.urls import path
from .views import TacheAPIView, TacheDetailAPIView

# Routes de l'application taches (accessibles en v1 et v2 depuis config/urls.py)
urlpatterns = [
    path('taches/', TacheAPIView.as_view(), name="taches_list"),
    path('taches/<int:pk>/', TacheDetailAPIView.as_view(), name="taches_detail"),
]
