from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.urls import reverse


class Departement(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.nom


class Enseignant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=15, blank=True)
    adresse = models.TextField(blank=True)
    date_embauche = models.DateField()
    avatar = models.ImageField(upload_to='avatars/enseignants/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    @property
    def nom_complet(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Classe(models.Model):
    NIVEAUX = [
        ('L1', 'Licence 1'),
        ('L2', 'Licence 2'),
        ('L3', 'Licence 3'),
        ('M1', 'Master 1'),
        ('M2', 'Master 2'),
    ]
    
    nom = models.CharField(max_length=50)
    niveau = models.CharField(max_length=2, choices=NIVEAUX)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nom} - {self.get_niveau_display()}"


class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    numero_etudiant = models.CharField(max_length=20, unique=True)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    date_naissance = models.DateField()
    telephone = models.CharField(max_length=15, blank=True)
    adresse = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/etudiants/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.numero_etudiant})"
    
    @property
    def nom_complet(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Matiere(models.Model):
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    credits = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.code} - {self.nom}"


class Cours(models.Model):
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    semestre = models.CharField(max_length=2, choices=[('S1', 'Semestre 1'), ('S2', 'Semestre 2')])
    annee_scolaire = models.CharField(max_length=9, help_text="Format: 2023-2024")
    
    class Meta:
        unique_together = ['matiere', 'classe', 'semestre', 'annee_scolaire']
    
    def __str__(self):
        return f"{self.matiere.nom} - {self.classe.nom} ({self.annee_scolaire})"


class Note(models.Model):
    TYPES_EVALUATION = [
        ('DS', 'Devoir Surveillé'),
        ('CC', 'Contrôle Continu'),
        ('TP', 'Travaux Pratiques'),
        ('PROJET', 'Projet'),
        ('EXAMEN', 'Examen Final'),
    ]
    
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    type_evaluation = models.CharField(max_length=10, choices=TYPES_EVALUATION)
    note = models.DecimalField(max_digits=4, decimal_places=2, 
                              validators=[MinValueValidator(0), MaxValueValidator(20)])
    coefficient = models.DecimalField(max_digits=3, decimal_places=1, default=1.0)
    date_evaluation = models.DateField()
    commentaire = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.etudiant.nom_complet} - {self.cours.matiere.nom} - {self.note}/20"


class EmploiDuTemps(models.Model):
    JOURS_SEMAINE = [
        ('LUNDI', 'Lundi'),
        ('MARDI', 'Mardi'),
        ('MERCREDI', 'Mercredi'),
        ('JEUDI', 'Jeudi'),
        ('VENDREDI', 'Vendredi'),
        ('SAMEDI', 'Samedi'),
    ]
    
    TYPES_COURS = [
        ('CM', 'Cours Magistral'),
        ('TD', 'Travaux Dirigés'),
        ('TP', 'Travaux Pratiques'),
    ]
    
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    jour = models.CharField(max_length=10, choices=JOURS_SEMAINE)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    type_cours = models.CharField(max_length=2, choices=TYPES_COURS)
    salle = models.CharField(max_length=20)
    
    class Meta:
        unique_together = ['cours', 'jour', 'heure_debut']
        ordering = ['jour', 'heure_debut']
    
    def __str__(self):
        return f"{self.cours.matiere.nom} - {self.jour} {self.heure_debut}-{self.heure_fin}"


# Nouveaux modèles pour la messagerie et notifications

class Message(models.Model):
    """Modèle pour la messagerie interne"""
    TYPES_MESSAGE = [
        ('ADMIN_TO_ALL', 'Admin vers Tous'),
        ('ADMIN_TO_TEACHER', 'Admin vers Enseignant'),
        ('ADMIN_TO_STUDENT', 'Admin vers Étudiant'),
        ('STUDENT_TO_TEACHER', 'Étudiant vers Enseignant'),
        ('STUDENT_TO_ADMIN', 'Étudiant vers Admin'),
        ('TEACHER_TO_ADMIN', 'Enseignant vers Admin'),
    ]
    
    expediteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_envoyes')
    destinataire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_recus', null=True, blank=True)
    type_message = models.CharField(max_length=20, choices=TYPES_MESSAGE)
    sujet = models.CharField(max_length=200)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(default=timezone.now)
    lu = models.BooleanField(default=False)
    important = models.BooleanField(default=False)
    
    # Pour les messages à tous
    pour_tous_enseignants = models.BooleanField(default=False)
    pour_tous_etudiants = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-date_envoi']
    
    def __str__(self):
        return f"{self.sujet} - {self.expediteur.username} -> {self.destinataire.username if self.destinataire else 'Tous'}"


class Notification(models.Model):
    """Modèle pour les notifications système"""
    TYPES_NOTIFICATION = [
        ('INFO', 'Information'),
        ('WARNING', 'Avertissement'),
        ('SUCCESS', 'Succès'),
        ('ERROR', 'Erreur'),
        ('NEW_MESSAGE', 'Nouveau message'),
        ('NEW_GRADE', 'Nouvelle note'),
        ('SCHEDULE_CHANGE', 'Changement emploi du temps'),
        ('ACCOUNT_CREATED', 'Compte créé'),
        ('PASSWORD_RESET', 'Mot de passe réinitialisé'),
    ]
    
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type_notification = models.CharField(max_length=20, choices=TYPES_NOTIFICATION)
    titre = models.CharField(max_length=200)
    message = models.TextField()
    date_creation = models.DateTimeField(default=timezone.now)
    lue = models.BooleanField(default=False)
    url_action = models.URLField(blank=True, null=True)  # URL vers laquelle rediriger
    
    class Meta:
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.titre} - {self.utilisateur.username}"


class ProfilUtilisateur(models.Model):
    """Profil étendu pour tous les utilisateurs"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    telephone = models.CharField(max_length=15, blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    
    # Paramètres de sécurité
    mot_de_passe_temporaire = models.BooleanField(default=True)
    dernier_mot_de_passe = models.CharField(max_length=255, blank=True, null=True, help_text="Dernier mot de passe défini (pour affichage admin)")
    compte_active = models.BooleanField(default=True)
    
    # Statistiques de connexion
    nombre_connexions = models.IntegerField(default=0)
    derniere_connexion_ip = models.GenericIPAddressField(blank=True, null=True)
    
    # Préférences
    theme = models.CharField(max_length=20, default='light')
    langue = models.CharField(max_length=10, default='fr')
    
    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return '/static/images/default-avatar.png'
    
    def __str__(self):
        return f"Profil de {self.user.get_full_name()}"


class HistoriqueConnexion(models.Model):
    """Historique des connexions utilisateurs"""
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='historique_connexions')
    date_connexion = models.DateTimeField(default=timezone.now)
    adresse_ip = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    succes = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-date_connexion']
    
    def __str__(self):
        return f"{self.utilisateur.username} - {self.date_connexion}"


class ParametresSysteme(models.Model):
    """Paramètres globaux du système"""
    nom_etablissement = models.CharField(max_length=200, default="EduManager")
    logo = models.ImageField(upload_to='system/', blank=True, null=True)
    adresse_etablissement = models.TextField(blank=True)
    telephone_etablissement = models.CharField(max_length=15, blank=True)
    email_etablissement = models.EmailField(blank=True)
    
    # Paramètres de sécurité
    duree_session = models.PositiveIntegerField(default=30)  # en minutes
    tentatives_connexion_max = models.PositiveIntegerField(default=5)
    
    # Paramètres de notification
    smtp_server = models.CharField(max_length=100, blank=True)
    smtp_port = models.PositiveIntegerField(default=587)
    smtp_username = models.CharField(max_length=100, blank=True)
    smtp_password = models.CharField(max_length=100, blank=True)
    smtp_use_tls = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Paramètres - {self.nom_etablissement}"
    
    class Meta:
        verbose_name = "Paramètres Système"
        verbose_name_plural = "Paramètres Système"
