from django.contrib import admin
from .models import (
    Departement, Enseignant, Classe, Etudiant, 
    Matiere, Cours, Note, EmploiDuTemps,
    Message, Notification, ProfilUtilisateur, 
    HistoriqueConnexion, ParametresSysteme
)


@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    list_display = ['nom', 'description']
    search_fields = ['nom']


@admin.register(Enseignant)
class EnseignantAdmin(admin.ModelAdmin):
    list_display = ['nom_complet', 'departement', 'telephone', 'date_embauche']
    list_filter = ['departement', 'date_embauche']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']


@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ['nom', 'niveau', 'departement']
    list_filter = ['niveau', 'departement']
    search_fields = ['nom']


@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ['nom_complet', 'numero_etudiant', 'classe', 'telephone']
    list_filter = ['classe', 'classe__niveau']
    search_fields = ['user__first_name', 'user__last_name', 'numero_etudiant']


@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ['code', 'nom', 'credits']
    search_fields = ['nom', 'code']


@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ['matiere', 'enseignant', 'classe', 'semestre', 'annee_scolaire']
    list_filter = ['semestre', 'annee_scolaire', 'classe__niveau']
    search_fields = ['matiere__nom', 'enseignant__user__last_name']


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['etudiant', 'cours', 'type_evaluation', 'note', 'date_evaluation']
    list_filter = ['type_evaluation', 'cours__matiere', 'date_evaluation']
    search_fields = ['etudiant__user__last_name', 'cours__matiere__nom']


@admin.register(EmploiDuTemps)
class EmploiDuTempsAdmin(admin.ModelAdmin):
    list_display = ['cours', 'jour', 'heure_debut', 'heure_fin', 'type_cours', 'salle']
    list_filter = ['jour', 'type_cours', 'cours__classe']
    search_fields = ['cours__matiere__nom', 'salle']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sujet', 'expediteur', 'destinataire', 'type_message', 'date_envoi', 'lu', 'important']
    list_filter = ['type_message', 'lu', 'important', 'date_envoi']
    search_fields = ['sujet', 'contenu', 'expediteur__username', 'destinataire__username']
    readonly_fields = ['date_envoi']
    
    def has_change_permission(self, request, obj=None):
        # Seul l'expéditeur ou un admin peut modifier
        if obj and not request.user.is_superuser:
            return obj.expediteur == request.user
        return True


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['titre', 'utilisateur', 'type_notification', 'date_creation', 'lue']
    list_filter = ['type_notification', 'lue', 'date_creation']
    search_fields = ['titre', 'message', 'utilisateur__username']
    readonly_fields = ['date_creation']


@admin.register(ProfilUtilisateur)
class ProfilUtilisateurAdmin(admin.ModelAdmin):
    list_display = ['user', 'telephone', 'compte_active', 'mot_de_passe_temporaire', 'nombre_connexions']
    list_filter = ['compte_active', 'mot_de_passe_temporaire', 'theme', 'langue']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'telephone']
    readonly_fields = ['nombre_connexions', 'derniere_connexion_ip']


@admin.register(HistoriqueConnexion)
class HistoriqueConnexionAdmin(admin.ModelAdmin):
    list_display = ['utilisateur', 'date_connexion', 'adresse_ip', 'succes']
    list_filter = ['succes', 'date_connexion']
    search_fields = ['utilisateur__username', 'adresse_ip']
    readonly_fields = ['date_connexion']
    
    def has_add_permission(self, request):
        return False  # Pas d'ajout manuel
    
    def has_change_permission(self, request, obj=None):
        return False  # Pas de modification


@admin.register(ParametresSysteme)
class ParametresSystemeAdmin(admin.ModelAdmin):
    list_display = ['nom_etablissement', 'email_etablissement', 'duree_session', 'tentatives_connexion_max']
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom_etablissement', 'logo', 'adresse_etablissement', 'telephone_etablissement', 'email_etablissement')
        }),
        ('Paramètres de sécurité', {
            'fields': ('duree_session', 'tentatives_connexion_max')
        }),
        ('Configuration SMTP', {
            'fields': ('smtp_server', 'smtp_port', 'smtp_username', 'smtp_password', 'smtp_use_tls'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Un seul objet de paramètres système
        return not ParametresSysteme.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False  # Pas de suppression
