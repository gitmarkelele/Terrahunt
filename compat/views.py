from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from compat.services.get_requests import get_client_demandes
from .models import ProfilCandidat, Demande, Correspondance
from .serializers import RegisterSerializer, DemandeSerializer, ProfilCandidatSerializer
from django.http import JsonResponse


# Mock function to replace AI service temporarily
def mock_evaluer_compatibilite(profil, demande):
    """Mock function that returns a simple score"""
    return "Score: 80% compatible. Justification: Profil et demande correspondent sur les compétences clés et l'expérience requise."

class EvaluerCompatibilite(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profil_id = request.data.get("profil_id")
        demande_id = request.data.get("demande_id")

        try:
            profil = ProfilCandidat.objects.get(id=profil_id)
            demande = Demande.objects.get(id=demande_id)

            score = mock_evaluer_compatibilite(str(profil), str(demande))
            
            # Extract numeric score for database storage
            score_numeric = 7.5  # Mock score
            
            Correspondance.objects.create(
                profil=profil,
                demande=demande,
                score_compatibilite=score_numeric
            )

            return Response({"score": score})
        except ProfilCandidat.DoesNotExist:
            return Response({"error": "Profil not found"}, status=status.HTTP_404_NOT_FOUND)
        except Demande.DoesNotExist:
            return Response({"error": "Demande not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Utilisateur créé avec succès."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


def fetch_demandes_view(request):
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        return JsonResponse({'error': 'Missing or invalid token'}, status=401)

    jwt_token = auth_header.split(' ')[1]

    demandes = get_client_demandes(jwt_token)

    if demandes is not None:
        return JsonResponse(demandes, safe=False)
    else:
        return JsonResponse({'error': 'Failed to fetch demandes'}, status=500)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class DemandeListView(generics.ListAPIView):
    queryset = Demande.objects.all().order_by('-date_creation')
    serializer_class = DemandeSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

class DemandeDetailView(generics.RetrieveAPIView):
    queryset = Demande.objects.all()
    serializer_class = DemandeSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

class ProfilListView(generics.ListAPIView):
    queryset = ProfilCandidat.objects.all().order_by('nom')
    serializer_class = ProfilCandidatSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

class ProfilDetailView(generics.RetrieveAPIView):
    queryset = ProfilCandidat.objects.all()
    serializer_class = ProfilCandidatSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
