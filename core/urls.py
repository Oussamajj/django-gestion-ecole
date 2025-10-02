from django.urls import path
from . import views

urlpatterns = [
    # Authentification
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Étudiants
    path('etudiants/', views.etudiants_list, name='etudiants_list'),
    path('etudiants/<int:pk>/', views.etudiant_detail, name='etudiant_detail'),
    path('etudiants/ajouter/', views.ajouter_etudiant, name='ajouter_etudiant'),
    path('etudiants/<int:pk>/modifier/', views.modifier_etudiant, name='modifier_etudiant'),
    path('etudiants/<int:pk>/supprimer/', views.supprimer_etudiant, name='supprimer_etudiant'),
    
    # Enseignants
    path('enseignants/', views.enseignants_list, name='enseignants_list'),
    path('enseignants/ajouter/', views.ajouter_enseignant, name='ajouter_enseignant'),
    path('enseignants/<int:pk>/modifier/', views.modifier_enseignant, name='modifier_enseignant'),
    path('enseignants/<int:pk>/supprimer/', views.supprimer_enseignant, name='supprimer_enseignant'),
    
    # Cours
    path('cours/', views.cours_list, name='cours_list'),
    path('cours/ajouter/', views.ajouter_cours, name='ajouter_cours'),
    path('cours/<int:pk>/modifier/', views.modifier_cours, name='modifier_cours'),
    path('cours/<int:pk>/supprimer/', views.supprimer_cours, name='supprimer_cours'),
    
    # Notes
    path('notes/', views.notes_list, name='notes_list'),
    path('notes/ajouter/', views.ajouter_note, name='ajouter_note'),
    path('notes/<int:pk>/modifier/', views.modifier_note, name='modifier_note'),
    path('notes/<int:pk>/supprimer/', views.supprimer_note, name='supprimer_note'),
    
    # Emploi du temps (vue calendrier)
    path('emploi-du-temps/', views.emploi_du_temps, name='emploi_du_temps'),
    
    # Statistiques
    path('statistiques/', views.statistiques, name='statistiques'),
    
    # Nouvelles fonctionnalités
    # Gestion des utilisateurs (admin uniquement)
    path('gestion-utilisateurs/', views.gestion_utilisateurs, name='gestion_utilisateurs'),
    path('gestion-utilisateurs/creer/', views.creer_utilisateur, name='creer_utilisateur'),
    path('gestion-utilisateurs/<int:user_id>/modifier/', views.modifier_utilisateur, name='modifier_utilisateur'),
    path('gestion-utilisateurs/<int:user_id>/reinitialiser-mot-de-passe/', views.reinitialiser_mot_de_passe, name='reinitialiser_mot_de_passe'),
    path('gestion-utilisateurs/<int:user_id>/toggle/', views.toggle_utilisateur, name='toggle_utilisateur'),
    path('gestion-utilisateurs/<int:user_id>/get-password/', views.get_user_password, name='get_user_password'),
    path('gestion-utilisateurs/<int:user_id>/set-password/', views.set_user_password, name='set_user_password'),
    
    # Messagerie
    path('messagerie/', views.messagerie, name='messagerie'),
    path('messagerie/envoyer/', views.envoyer_message, name='envoyer_message'),
    
    # Notifications
    path('notifications/', views.notifications, name='notifications'),
    
    # Profil utilisateur
    path('profil/mot-de-passe/', views.changer_mot_de_passe, name='changer_mot_de_passe'),
    
    # Comptes de test (admin uniquement)
    path('comptes-test/', views.comptes_test, name='comptes_test'),
    path('reinitialiser-mot-de-passe/<int:user_id>/', views.reinitialiser_mot_de_passe_utilisateur, name='reinitialiser_mot_de_passe_utilisateur'),
    path('reinitialiser-tous-mots-de-passe/', views.reinitialiser_tous_mots_de_passe, name='reinitialiser_tous_mots_de_passe'),
    path('generer-mot-de-passe/<int:user_id>/', views.generer_mot_de_passe_aleatoire, name='generer_mot_de_passe_aleatoire'),
    
    # Emploi du temps (gestion complète)
    path('emploi-du-temps/gestion/', views.emploi_du_temps_list, name='emploi_du_temps_list'),
    path('emploi-du-temps/ajouter/', views.ajouter_emploi_du_temps, name='ajouter_emploi_du_temps'),
    path('emploi-du-temps/<int:pk>/modifier/', views.modifier_emploi_du_temps, name='modifier_emploi_du_temps'),
    path('emploi-du-temps/<int:pk>/supprimer/', views.supprimer_emploi_du_temps, name='supprimer_emploi_du_temps'),
]
