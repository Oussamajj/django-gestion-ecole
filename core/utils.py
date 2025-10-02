"""
Utilitaires pour EduManager
"""
import secrets
import string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import Notification, ProfilUtilisateur, HistoriqueConnexion


def generer_mot_de_passe(longueur=8):
    """Génère un mot de passe aléatoire sécurisé"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    mot_de_passe = ''.join(secrets.choice(alphabet) for _ in range(longueur))
    return mot_de_passe


def generer_identifiant(prenom, nom, type_utilisateur='etudiant'):
    """Génère un identifiant unique"""
    if type_utilisateur == 'etudiant':
        base = f"{prenom.lower()}.{nom.lower()}"
    else:
        base = f"{prenom.lower()}.{nom.lower()}"
    
    # Vérifier l'unicité
    compteur = 1
    identifiant = base
    while User.objects.filter(username=identifiant).exists():
        identifiant = f"{base}{compteur}"
        compteur += 1
    
    return identifiant


def envoyer_notification(utilisateur, type_notif, titre, message, url_action=None):
    """Crée une notification pour un utilisateur"""
    notification = Notification.objects.create(
        utilisateur=utilisateur,
        type_notification=type_notif,
        titre=titre,
        message=message,
        url_action=url_action
    )
    return notification


def envoyer_email_bienvenue(user, mot_de_passe_temporaire):
    """Envoie un email de bienvenue avec les identifiants"""
    sujet = "Bienvenue sur EduManager - Vos identifiants de connexion"
    
    message = f"""
Bonjour {user.first_name} {user.last_name},

Votre compte EduManager a été créé avec succès !

Vos identifiants de connexion :
- Identifiant : {user.username}
- Mot de passe temporaire : {mot_de_passe_temporaire}

⚠️ IMPORTANT : Vous devrez changer votre mot de passe lors de votre première connexion.

Connectez-vous sur : {settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://localhost:8000'}

Cordialement,
L'équipe EduManager
"""
    
    try:
        send_mail(
            sujet,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Erreur envoi email : {e}")
        return False


def creer_profil_utilisateur(user):
    """Crée un profil utilisateur s'il n'existe pas"""
    profil, created = ProfilUtilisateur.objects.get_or_create(
        user=user,
        defaults={
            'mot_de_passe_temporaire': True,
            'compte_active': True,
        }
    )
    return profil


def enregistrer_connexion(user, request, succes=True):
    """Enregistre une tentative de connexion"""
    ip = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    HistoriqueConnexion.objects.create(
        utilisateur=user,
        adresse_ip=ip,
        user_agent=user_agent,
        succes=succes
    )
    
    if succes:
        # Mettre à jour le profil
        profil = creer_profil_utilisateur(user)
        profil.derniere_connexion_ip = ip
        profil.nombre_connexions += 1
        profil.save()


def get_client_ip(request):
    """Récupère l'IP du client"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def compter_messages_non_lus(user):
    """Compte les messages non lus d'un utilisateur"""
    from .models import Message
    return Message.objects.filter(
        destinataire=user,
        lu=False
    ).count()


def compter_notifications_non_lues(user):
    """Compte les notifications non lues d'un utilisateur"""
    return Notification.objects.filter(
        utilisateur=user,
        lue=False
    ).count()


def get_user_type(user):
    """Détermine le type d'utilisateur"""
    if user.is_superuser:
        return 'admin'
    elif hasattr(user, 'enseignant'):
        return 'enseignant'
    elif hasattr(user, 'etudiant'):
        return 'etudiant'
    else:
        return 'autre'


def peut_envoyer_message(expediteur, destinataire):
    """Vérifie si un utilisateur peut envoyer un message à un autre"""
    exp_type = get_user_type(expediteur)
    dest_type = get_user_type(destinataire)
    
    # Admin peut envoyer à tout le monde
    if exp_type == 'admin':
        return True
    
    # Étudiant peut envoyer à admin et ses enseignants
    if exp_type == 'etudiant':
        if dest_type == 'admin':
            return True
        if dest_type == 'enseignant':
            # Vérifier si l'enseignant enseigne à cet étudiant
            from .models import Cours
            etudiant = expediteur.etudiant
            return Cours.objects.filter(
                enseignant__user=destinataire,
                classe=etudiant.classe
            ).exists()
    
    # Enseignant peut envoyer à admin et ses étudiants
    if exp_type == 'enseignant':
        if dest_type == 'admin':
            return True
        if dest_type == 'etudiant':
            # Vérifier si l'enseignant enseigne à cet étudiant
            from .models import Cours
            enseignant = expediteur.enseignant
            etudiant = destinataire.etudiant
            return Cours.objects.filter(
                enseignant=enseignant,
                classe=etudiant.classe
            ).exists()
    
    return False
