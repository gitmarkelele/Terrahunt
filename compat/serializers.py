from rest_framework import serializers
from .models import Utilisateur, Demande, ProfilCandidat

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Utilisateur
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        return Utilisateur.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )

class DemandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demande
        fields = '__all__'

class ProfilCandidatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilCandidat
        fields = '__all__'