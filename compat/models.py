import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# -------------------------------
# Enums
# -------------------------------

class StatutProfil(models.TextChoices):
    PROSPECTION = "Prospection"
    INVITE = "Invite"
    INSCRIT = "Inscrit"

class StatutDemande(models.TextChoices):
    EN_ATTENTE = "EnAttente"
    EN_COURS = "EnCours"
    SATISFAITE = "Satisfaite"
    NON_SATISFAITE = "NonSatisfaite"

class PlateformeType(models.TextChoices):
    SCRAPPING = "Scrapping"
    API = "API"

# -------------------------------
# Utilisateur (custom user)
# -------------------------------

class UtilisateurManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Utilisateur(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UtilisateurManager()

    def __str__(self):
        return self.email

# -------------------------------
# ProfilCandidat
# -------------------------------

class ProfilCandidat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    source = models.CharField(max_length=255)
    statut = models.CharField(max_length=20, choices=StatutProfil.choices)

    prospecte_par = models.ForeignKey(Utilisateur, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

# -------------------------------
# Demande
# -------------------------------

class Demande(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titre = models.CharField(max_length=255)
    client = models.CharField(max_length=255)
    description = models.TextField()
    statut = models.CharField(max_length=20, choices=StatutDemande.choices)
    date_creation = models.DateTimeField(auto_now_add=True)
    autre = models.TextField(blank=True)

    def __str__(self):
        return self.titre

# -------------------------------
# Message
# -------------------------------

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contenu = models.TextField()
    date_generation = models.DateTimeField(auto_now_add=True)
    envoi_automatique = models.BooleanField(default=False)

    profil = models.ForeignKey(ProfilCandidat, on_delete=models.CASCADE, related_name="messages")
    demande = models.ForeignKey(Demande, on_delete=models.CASCADE, related_name="messages")

# -------------------------------
# Competence
# -------------------------------

class Competence(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=255)

    def __str__(self):
        return self.nom

# -------------------------------
# Langue
# -------------------------------

class Langue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

# -------------------------------
# Plateforme
# -------------------------------

class Plateforme(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=PlateformeType.choices)

    candidats = models.ManyToManyField(ProfilCandidat, related_name="plateformes")

    def __str__(self):
        return self.nom

# -------------------------------
# Correspondance
# -------------------------------

class Correspondance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profil = models.ForeignKey(ProfilCandidat, on_delete=models.CASCADE, related_name="correspondances")
    demande = models.ForeignKey(Demande, on_delete=models.CASCADE, related_name="correspondances")
    score_compatibilite = models.FloatField()

# -------------------------------
# DemandeCompetence
# -------------------------------

class DemandeCompetence(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    demande = models.ForeignKey(Demande, on_delete=models.CASCADE, related_name="besoins")
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE)
    experience = models.CharField(max_length=255)

# -------------------------------
# ProfilCompetence
# -------------------------------

class ProfilCompetence(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profil = models.ForeignKey(ProfilCandidat, on_delete=models.CASCADE, related_name="competences")
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE)
    experience = models.CharField(max_length=255)

# -------------------------------
# ProfilLangue
# -------------------------------

class ProfilLangue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profil = models.ForeignKey(ProfilCandidat, on_delete=models.CASCADE, related_name="langues")
    langue = models.ForeignKey(Langue, on_delete=models.CASCADE)