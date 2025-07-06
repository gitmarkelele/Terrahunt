from django.urls import path
from .views import (
    EvaluerCompatibilite, RegisterAPIView, fetch_demandes_view,
    DemandeListView, DemandeDetailView,
    ProfilListView, ProfilDetailView,
    LogoutView,
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('evaluer-compatibilite/', EvaluerCompatibilite.as_view(), name='evaluer_compatibilite'),
    path('fetch-demandes/', fetch_demandes_view, name='fetch_demandes'),

    path('demandes/', DemandeListView.as_view(), name='demandes-list'),
    path('demandes/<uuid:id>/', DemandeDetailView.as_view(), name='demande-detail'),

    path('profils/', ProfilListView.as_view(), name='profils-list'),
    path('profils/<uuid:id>/', ProfilDetailView.as_view(), name='profil-detail'),

    path('logout/', LogoutView.as_view(), name='logout'),
]
