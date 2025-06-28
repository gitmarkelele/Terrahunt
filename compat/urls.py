from django.urls import path
from .views import EvaluerCompatibilite, RegisterAPIView, fetch_demandes_view

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('evaluer-compatibilite/', EvaluerCompatibilite.as_view(), name='evaluer_compatibilite'),
    path('fetch-demandes/', fetch_demandes_view, name='fetch_demandes'),
]
