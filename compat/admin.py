from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Utilisateur, ProfilCandidat, Demande, Message, Competence, 
    Langue, Plateforme, Correspondance, DemandeCompetence, 
    ProfilCompetence, ProfilLangue
)

@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'username')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

@admin.register(ProfilCandidat)
class ProfilCandidatAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'email', 'statut', 'source')
    list_filter = ('statut', 'source')
    search_fields = ('nom', 'prenom', 'email')

@admin.register(Demande)
class DemandeAdmin(admin.ModelAdmin):
    list_display = ('titre', 'client', 'statut', 'date_creation')
    list_filter = ('statut', 'date_creation')
    search_fields = ('titre', 'client')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('profil', 'demande', 'date_generation', 'envoi_automatique')
    list_filter = ('envoi_automatique', 'date_generation')

@admin.register(Competence)
class CompetenceAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)

@admin.register(Langue)
class LangueAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)

@admin.register(Plateforme)
class PlateformeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type')
    list_filter = ('type',)

@admin.register(Correspondance)
class CorrespondanceAdmin(admin.ModelAdmin):
    list_display = ('profil', 'demande', 'score_compatibilite')
    list_filter = ('score_compatibilite',)

@admin.register(DemandeCompetence)
class DemandeCompetenceAdmin(admin.ModelAdmin):
    list_display = ('demande', 'competence', 'experience')

@admin.register(ProfilCompetence)
class ProfilCompetenceAdmin(admin.ModelAdmin):
    list_display = ('profil', 'competence', 'experience')

@admin.register(ProfilLangue)
class ProfilLangueAdmin(admin.ModelAdmin):
    list_display = ('profil', 'langue')