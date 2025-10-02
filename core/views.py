from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from .models import (
    Etudiant, Enseignant, Classe, Cours, Note, 
    EmploiDuTemps, Matiere, Departement, Message, 
    Notification, ProfilUtilisateur, ParametresSysteme
)
from .forms import (
    LoginForm, EtudiantForm, EnseignantForm, CoursForm, 
    NoteForm, EmploiDuTempsForm, MessageForm, 
    ChangerMotDePasseForm, CreerUtilisateurForm
)
from .utils import (
    generer_mot_de_passe, generer_identifiant, envoyer_notification,
    envoyer_email_bienvenue, creer_profil_utilisateur, enregistrer_connexion,
    compter_messages_non_lus, compter_notifications_non_lues, get_user_type
)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    else:
        form = LoginForm()
    
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    from django.utils import timezone
    from datetime import datetime, timedelta
    from django.db.models import Avg
    
    context = {}
    
    # Statistiques générales (toujours disponibles)
    context['total_etudiants'] = Etudiant.objects.count()
    context['total_enseignants'] = Enseignant.objects.count()
    context['total_cours'] = Cours.objects.count()
    context['total_classes'] = Classe.objects.count()
    
    # Statistiques d'activité avec gestion d'erreurs
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    
    # Connexions récentes (avec gestion d'erreur si le modèle n'existe pas)
    try:
        context['connexions_aujourd_hui'] = HistoriqueConnexion.objects.filter(
            date_connexion__date=today, succes=True
        ).count()
        context['connexions_semaine'] = HistoriqueConnexion.objects.filter(
            date_connexion__date__gte=week_ago, succes=True
        ).count()
        context['utilisateurs_actifs'] = HistoriqueConnexion.objects.filter(
            date_connexion__date__gte=week_ago, succes=True
        ).values('utilisateur').distinct().count()
    except:
        context['connexions_aujourd_hui'] = 0
        context['connexions_semaine'] = 0
        context['utilisateurs_actifs'] = 0
    
    # Notes récentes
    try:
        context['notes_ajoutees_semaine'] = Note.objects.filter(
            date_creation__date__gte=week_ago
        ).count()
    except:
        context['notes_ajoutees_semaine'] = 0
    
    # Messages récents
    try:
        context['messages_semaine'] = Message.objects.filter(
            date_envoi__date__gte=week_ago
        ).count()
    except:
        context['messages_semaine'] = 0
    
    # Mots de passe temporaires
    try:
        context['mots_de_passe_temporaires'] = ProfilUtilisateur.objects.filter(
            mot_de_passe_temporaire=True
        ).count()
    except:
        context['mots_de_passe_temporaires'] = 0
    
    # Données spécifiques selon le type d'utilisateur
    try:
        etudiant = Etudiant.objects.get(user=request.user)
        context['user_type'] = 'etudiant'
        context['etudiant'] = etudiant
        context['mes_cours'] = Cours.objects.filter(classe=etudiant.classe)
        context['mes_notes'] = Note.objects.filter(etudiant=etudiant).order_by('-date_evaluation')[:5]
        
        # Emploi du temps avec gestion d'erreur
        try:
            context['emploi_du_temps'] = EmploiDuTemps.objects.filter(
                cours__classe=etudiant.classe
            ).order_by('jour', 'heure_debut')
        except:
            context['emploi_du_temps'] = []
        
        # Moyenne générale de l'étudiant
        notes_etudiant = Note.objects.filter(etudiant=etudiant)
        if notes_etudiant.exists():
            context['moyenne_generale'] = notes_etudiant.aggregate(Avg('valeur'))['valeur__avg']
        
    except Etudiant.DoesNotExist:
        try:
            enseignant = Enseignant.objects.get(user=request.user)
            context['user_type'] = 'enseignant'
            context['enseignant'] = enseignant
            context['mes_cours'] = Cours.objects.filter(enseignant=enseignant)
            
            # Emploi du temps avec gestion d'erreur
            try:
                context['emploi_du_temps'] = EmploiDuTemps.objects.filter(
                    cours__enseignant=enseignant
                ).order_by('jour', 'heure_debut')
            except:
                context['emploi_du_temps'] = []
            
            # Statistiques pour l'enseignant
            context['mes_etudiants'] = Note.objects.filter(
                cours__enseignant=enseignant
            ).values('etudiant').distinct().count()
            
        except Enseignant.DoesNotExist:
            context['user_type'] = 'admin'
            
            # Statistiques supplémentaires pour l'admin
            try:
                context['notifications_non_lues'] = Notification.objects.filter(lue=False).count()
                context['messages_non_lus'] = Message.objects.filter(lu=False).count()
            except:
                context['notifications_non_lues'] = 0
                context['messages_non_lus'] = 0
    
    return render(request, 'core/dashboard.html', context)


@login_required
def etudiants_list(request):
    etudiants = Etudiant.objects.select_related('user', 'classe').all()
    
    # Recherche
    search = request.GET.get('search')
    if search:
        etudiants = etudiants.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(numero_etudiant__icontains=search)
        )
    
    # Filtrage par classe
    classe_id = request.GET.get('classe')
    if classe_id:
        etudiants = etudiants.filter(classe_id=classe_id)
    
    paginator = Paginator(etudiants, 20)
    page = request.GET.get('page')
    etudiants = paginator.get_page(page)
    
    classes = Classe.objects.all()
    
    return render(request, 'core/etudiants_list.html', {
        'etudiants': etudiants,
        'classes': classes,
        'search': search,
        'classe_id': classe_id
    })


@login_required
def etudiant_detail(request, pk):
    etudiant = get_object_or_404(Etudiant, pk=pk)
    notes = Note.objects.filter(etudiant=etudiant).order_by('-date_evaluation')
    cours = Cours.objects.filter(classe=etudiant.classe)
    
    return render(request, 'core/etudiant_detail.html', {
        'etudiant': etudiant,
        'notes': notes,
        'cours': cours
    })


@login_required
def enseignants_list(request):
    enseignants = Enseignant.objects.select_related('user', 'departement').all()
    
    search = request.GET.get('search')
    if search:
        enseignants = enseignants.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search)
        )
    
    paginator = Paginator(enseignants, 20)
    page = request.GET.get('page')
    enseignants = paginator.get_page(page)
    
    return render(request, 'core/enseignants_list.html', {
        'enseignants': enseignants,
        'search': search
    })


@login_required
def cours_list(request):
    cours = Cours.objects.select_related('matiere', 'enseignant', 'classe').all()
    
    search = request.GET.get('search')
    if search:
        cours = cours.filter(
            Q(matiere__nom__icontains=search) |
            Q(enseignant__user__last_name__icontains=search)
        )
    
    paginator = Paginator(cours, 20)
    page = request.GET.get('page')
    cours = paginator.get_page(page)
    
    return render(request, 'core/cours_list.html', {
        'cours': cours,
        'search': search
    })


@login_required
def notes_list(request):
    notes = Note.objects.select_related('etudiant', 'cours').all()
    
    # Filtrage par étudiant
    etudiant_id = request.GET.get('etudiant')
    if etudiant_id:
        notes = notes.filter(etudiant_id=etudiant_id)
    
    # Filtrage par cours
    cours_id = request.GET.get('cours')
    if cours_id:
        notes = notes.filter(cours_id=cours_id)
    
    paginator = Paginator(notes, 20)
    page = request.GET.get('page')
    notes = paginator.get_page(page)
    
    etudiants = Etudiant.objects.all()
    cours = Cours.objects.all()
    
    return render(request, 'core/notes_list.html', {
        'notes': notes,
        'etudiants': etudiants,
        'cours': cours,
        'etudiant_id': etudiant_id,
        'cours_id': cours_id
    })


@login_required
def emploi_du_temps(request):
    emplois = EmploiDuTemps.objects.select_related('cours').all()
    
    # Filtrage par classe
    classe_id = request.GET.get('classe')
    if classe_id:
        emplois = emplois.filter(cours__classe_id=classe_id)
    
    # Filtrage par enseignant
    enseignant_id = request.GET.get('enseignant')
    if enseignant_id:
        emplois = emplois.filter(cours__enseignant_id=enseignant_id)
    
    # Organisation par jour
    emploi_par_jour = {}
    for emploi in emplois:
        if emploi.jour not in emploi_par_jour:
            emploi_par_jour[emploi.jour] = []
        emploi_par_jour[emploi.jour].append(emploi)
    
    classes = Classe.objects.all()
    enseignants = Enseignant.objects.all()
    
    return render(request, 'core/emploi_du_temps.html', {
        'emploi_par_jour': emploi_par_jour,
        'classes': classes,
        'enseignants': enseignants,
        'classe_id': classe_id,
        'enseignant_id': enseignant_id
    })


@login_required
def statistiques(request):
    # Statistiques par classe
    stats_classes = []
    for classe in Classe.objects.all():
        etudiants_count = Etudiant.objects.filter(classe=classe).count()
        moyenne_generale = Note.objects.filter(
            etudiant__classe=classe
        ).aggregate(Avg('note'))['note__avg']
        
        stats_classes.append({
            'classe': classe,
            'etudiants_count': etudiants_count,
            'moyenne_generale': round(moyenne_generale or 0, 2)
        })
    
    # Statistiques par matière
    stats_matieres = []
    for matiere in Matiere.objects.all():
        moyenne_matiere = Note.objects.filter(
            cours__matiere=matiere
        ).aggregate(Avg('note'))['note__avg']
        
        stats_matieres.append({
            'matiere': matiere,
            'moyenne': round(moyenne_matiere or 0, 2)
        })
    
    return render(request, 'core/statistiques.html', {
        'stats_classes': stats_classes,
        'stats_matieres': stats_matieres
    })


# Nouvelles vues pour la gestion avancée

def is_admin(user):
    """Vérifie si l'utilisateur est admin"""
    return user.is_authenticated and user.is_superuser

@login_required
def gestion_utilisateurs(request):
    """Vue pour gérer tous les utilisateurs (admin uniquement)"""
    # Vérifier que l'utilisateur est admin
    if not request.user.is_superuser:
        messages.error(request, 'Accès non autorisé. Vous devez être administrateur.')
        return redirect('dashboard')
    
    try:
        # Récupérer tous les utilisateurs
        utilisateurs = User.objects.all().order_by('date_joined')
        
        # Filtres
        search = request.GET.get('search', '')
        type_user = request.GET.get('type', '')
        
        if search:
            utilisateurs = utilisateurs.filter(
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
        
        if type_user == 'admin':
            utilisateurs = utilisateurs.filter(is_superuser=True)
        elif type_user == 'enseignant':
            utilisateurs = utilisateurs.filter(enseignant__isnull=False)
        elif type_user == 'etudiant':
            utilisateurs = utilisateurs.filter(etudiant__isnull=False)
        
        # Pagination
        paginator = Paginator(utilisateurs, 20)
        page = request.GET.get('page')
        utilisateurs = paginator.get_page(page)
        
        return render(request, 'core/gestion_utilisateurs.html', {
            'utilisateurs': utilisateurs,
            'search': search,
            'type_user': type_user
        })
    except Exception as e:
        messages.error(request, f'Erreur lors du chargement des utilisateurs: {str(e)}')
        return redirect('dashboard')


@login_required
def creer_utilisateur(request):
    """Créer un nouvel utilisateur (admin uniquement)"""
    # Vérifier que l'utilisateur est admin
    if not request.user.is_superuser:
        messages.error(request, 'Accès non autorisé. Vous devez être administrateur.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CreerUtilisateurForm(request.POST)
        if form.is_valid():
            # Créer l'utilisateur
            user = form.save(commit=False)
            
            # Générer identifiant et mot de passe
            identifiant = generer_identifiant(
                user.first_name, 
                user.last_name, 
                form.cleaned_data['type_utilisateur']
            )
            mot_de_passe = generer_mot_de_passe()
            
            user.username = identifiant
            user.set_password(mot_de_passe)
            user.save()
            
            # Créer le profil
            profil = creer_profil_utilisateur(user)
            profil.telephone = form.cleaned_data.get('telephone', '')
            profil.adresse = form.cleaned_data.get('adresse', '')
            profil.date_naissance = form.cleaned_data.get('date_naissance')
            profil.mot_de_passe_temporaire = True
            profil.save()
            
            # Créer le profil spécifique selon le type
            type_utilisateur = form.cleaned_data['type_utilisateur']
            
            if type_utilisateur == 'etudiant':
                numero = form.cleaned_data.get('numero_etudiant')
                if not numero:
                    # Générer un numéro automatique
                    derniere_numero = Etudiant.objects.filter(
                        numero_etudiant__startswith='ET'
                    ).count()
                    numero = f'ET{derniere_numero + 1:03d}'
                
                Etudiant.objects.create(
                    user=user,
                    numero_etudiant=numero,
                    classe=form.cleaned_data['classe'],
                    date_naissance=form.cleaned_data.get('date_naissance'),
                    telephone=form.cleaned_data.get('telephone', ''),
                    adresse=form.cleaned_data.get('adresse', '')
                )
                
            elif type_utilisateur == 'enseignant':
                Enseignant.objects.create(
                    user=user,
                    departement=form.cleaned_data['departement'],
                    date_embauche=form.cleaned_data.get('date_embauche', timezone.now().date()),
                    telephone=form.cleaned_data.get('telephone', ''),
                    adresse=form.cleaned_data.get('adresse', '')
                )
            
            # Envoyer notification
            envoyer_notification(
                user,
                'ACCOUNT_CREATED',
                'Compte créé',
                f'Votre compte a été créé. Identifiant: {identifiant}'
            )
            
            # Envoyer email si demandé
            if form.cleaned_data.get('envoyer_email') and user.email:
                envoyer_email_bienvenue(user, mot_de_passe)
            
            messages.success(
                request, 
                f'Utilisateur {user.get_full_name()} créé avec succès. '
                f'Identifiant: {identifiant}, Mot de passe: {mot_de_passe}'
            )
            return redirect('gestion_utilisateurs')
    else:
        form = CreerUtilisateurForm()
    
    return render(request, 'core/creer_utilisateur.html', {'form': form})


@login_required
def messagerie(request):
    """Vue principale de la messagerie"""
    # Messages reçus
    messages_recus = Message.objects.filter(
        Q(destinataire=request.user) |
        Q(pour_tous_enseignants=True, destinataire__isnull=True) & Q(expediteur__is_superuser=True) |
        Q(pour_tous_etudiants=True, destinataire__isnull=True) & Q(expediteur__is_superuser=True)
    ).order_by('-date_envoi')
    
    # Filtrer selon le type d'utilisateur
    user_type = get_user_type(request.user)
    if user_type == 'enseignant':
        messages_recus = messages_recus.filter(
            Q(destinataire=request.user) |
            Q(pour_tous_enseignants=True, destinataire__isnull=True)
        )
    elif user_type == 'etudiant':
        messages_recus = messages_recus.filter(
            Q(destinataire=request.user) |
            Q(pour_tous_etudiants=True, destinataire__isnull=True)
        )
    
    # Messages envoyés
    messages_envoyes = Message.objects.filter(
        expediteur=request.user
    ).order_by('-date_envoi')
    
    # Pagination
    paginator_recus = Paginator(messages_recus, 10)
    page_recus = request.GET.get('page_recus')
    messages_recus = paginator_recus.get_page(page_recus)
    
    paginator_envoyes = Paginator(messages_envoyes, 10)
    page_envoyes = request.GET.get('page_envoyes')
    messages_envoyes = paginator_envoyes.get_page(page_envoyes)
    
    return render(request, 'core/messagerie.html', {
        'messages_recus': messages_recus,
        'messages_envoyes': messages_envoyes,
        'user_type': user_type
    })


@login_required
def envoyer_message(request):
    """Envoyer un nouveau message"""
    if request.method == 'POST':
        form = MessageForm(user=request.user, data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.expediteur = request.user
            
            # Déterminer le type de message
            user_type = get_user_type(request.user)
            if user_type == 'admin':
                if form.cleaned_data.get('envoyer_a_tous_enseignants'):
                    message.type_message = 'ADMIN_TO_ALL'
                    message.pour_tous_enseignants = True
                elif form.cleaned_data.get('envoyer_a_tous_etudiants'):
                    message.type_message = 'ADMIN_TO_ALL'
                    message.pour_tous_etudiants = True
                else:
                    message.type_message = 'ADMIN_TO_TEACHER'  # Par défaut
            elif user_type == 'enseignant':
                message.type_message = 'TEACHER_TO_ADMIN'
            elif user_type == 'etudiant':
                message.type_message = 'STUDENT_TO_TEACHER'
            
            message.save()
            
            # Envoyer à des destinataires spécifiques
            destinataires = form.cleaned_data.get('destinataires')
            if destinataires:
                for destinataire in destinataires:
                    Message.objects.create(
                        expediteur=request.user,
                        destinataire=destinataire,
                        type_message=message.type_message,
                        sujet=message.sujet,
                        contenu=message.contenu,
                        important=message.important
                    )
                    
                    # Créer notification
                    envoyer_notification(
                        destinataire,
                        'NEW_MESSAGE',
                        'Nouveau message',
                        f'Vous avez reçu un message de {request.user.get_full_name()}'
                    )
            
            messages.success(request, 'Message envoyé avec succès!')
            return redirect('messagerie')
    else:
        form = MessageForm(user=request.user)
    
    return render(request, 'core/envoyer_message.html', {'form': form})


@login_required
def notifications(request):
    """Vue des notifications utilisateur"""
    notifications_list = Notification.objects.filter(
        utilisateur=request.user
    ).order_by('-date_creation')
    
    # Marquer comme lues si demandé
    if request.GET.get('mark_read'):
        notifications_list.update(lue=True)
        return redirect('notifications')
    
    # Pagination
    paginator = Paginator(notifications_list, 15)
    page = request.GET.get('page')
    notifications_list = paginator.get_page(page)
    
    return render(request, 'core/notifications.html', {
        'notifications': notifications_list
    })


@login_required
def changer_mot_de_passe(request):
    """Changer le mot de passe utilisateur"""
    if request.method == 'POST':
        form = ChangerMotDePasseForm(user=request.user, data=request.POST)
        if form.is_valid():
            nouveau_mdp = form.cleaned_data['nouveau_mot_de_passe']
            request.user.set_password(nouveau_mdp)
            request.user.save()
            
            # Mettre à jour le profil
            profil = creer_profil_utilisateur(request.user)
            profil.mot_de_passe_temporaire = False
            profil.save()
            
            # Créer notification
            envoyer_notification(
                request.user,
                'PASSWORD_RESET',
                'Mot de passe modifié',
                'Votre mot de passe a été modifié avec succès.'
            )
            
            messages.success(request, 'Mot de passe modifié avec succès!')
            return redirect('dashboard')
    else:
        form = ChangerMotDePasseForm(user=request.user)
    
    return render(request, 'core/changer_mot_de_passe.html', {'form': form})


# Vues CRUD pour les Étudiants

@login_required
def ajouter_etudiant(request):
    """Ajouter un nouvel étudiant (admin uniquement)"""
    if not request.user.is_superuser:
        messages.error(request, 'Accès non autorisé. Seuls les administrateurs peuvent ajouter des étudiants.')
        return redirect('etudiants_list')
        
    if request.method == 'POST':
        form = EtudiantForm(request.POST)
        if form.is_valid():
            # Créer l'utilisateur d'abord
            user = User.objects.create_user(
                username=form.cleaned_data.get('numero_etudiant', f"etudiant_{Etudiant.objects.count() + 1}"),
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                password='etudiant123'  # Mot de passe par défaut
            )
            
            # Créer l'étudiant
            etudiant = form.save(commit=False)
            etudiant.user = user
            etudiant.save()
            
            # Créer le profil
            creer_profil_utilisateur(user)
            
            messages.success(request, f'Étudiant {user.get_full_name()} ajouté avec succès!')
            return redirect('etudiants_list')
    else:
        form = EtudiantForm()
    
    return render(request, 'core/ajouter_etudiant.html', {'form': form})


@login_required
def modifier_etudiant(request, pk):
    """Modifier un étudiant"""
    etudiant = get_object_or_404(Etudiant, pk=pk)
    
    if request.method == 'POST':
        form = EtudiantForm(request.POST, instance=etudiant)
        if form.is_valid():
            # Mettre à jour l'utilisateur
            user = etudiant.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            
            # Mettre à jour l'étudiant
            form.save()
            
            messages.success(request, f'Étudiant {user.get_full_name()} modifié avec succès!')
            return redirect('etudiant_detail', pk=pk)
    else:
        # Pré-remplir le formulaire
        initial_data = {
            'first_name': etudiant.user.first_name,
            'last_name': etudiant.user.last_name,
            'email': etudiant.user.email,
        }
        form = EtudiantForm(instance=etudiant, initial=initial_data)
    
    return render(request, 'core/modifier_etudiant.html', {
        'form': form,
        'etudiant': etudiant
    })


@login_required
def supprimer_etudiant(request, pk):
    """Supprimer un étudiant"""
    etudiant = get_object_or_404(Etudiant, pk=pk)
    
    if request.method == 'POST':
        nom_complet = etudiant.user.get_full_name()
        etudiant.user.delete()  # Cela supprimera aussi l'étudiant par cascade
        messages.success(request, f'Étudiant {nom_complet} supprimé avec succès!')
        return redirect('etudiants_list')
    
    return render(request, 'core/supprimer_etudiant.html', {'etudiant': etudiant})


# Vues CRUD pour les Enseignants

@login_required
def ajouter_enseignant(request):
    """Ajouter un nouvel enseignant (admin uniquement)"""
    if not request.user.is_superuser:
        messages.error(request, 'Accès non autorisé. Seuls les administrateurs peuvent ajouter des enseignants.')
        return redirect('enseignants_list')
        
    if request.method == 'POST':
        form = EnseignantForm(request.POST)
        if form.is_valid():
            # Créer l'utilisateur d'abord
            user = User.objects.create_user(
                username=f"prof_{Enseignant.objects.count() + 1}",
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                password='prof123'  # Mot de passe par défaut
            )
            
            # Créer l'enseignant
            enseignant = form.save(commit=False)
            enseignant.user = user
            enseignant.save()
            
            # Créer le profil
            creer_profil_utilisateur(user)
            
            messages.success(request, f'Enseignant {user.get_full_name()} ajouté avec succès!')
            return redirect('enseignants_list')
    else:
        form = EnseignantForm()
    
    return render(request, 'core/ajouter_enseignant.html', {'form': form})


@login_required
def modifier_enseignant(request, pk):
    """Modifier un enseignant"""
    enseignant = get_object_or_404(Enseignant, pk=pk)
    
    if request.method == 'POST':
        form = EnseignantForm(request.POST, instance=enseignant)
        if form.is_valid():
            # Mettre à jour l'utilisateur
            user = enseignant.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            
            # Mettre à jour l'enseignant
            form.save()
            
            messages.success(request, f'Enseignant {user.get_full_name()} modifié avec succès!')
            return redirect('enseignants_list')
    else:
        # Pré-remplir le formulaire
        initial_data = {
            'first_name': enseignant.user.first_name,
            'last_name': enseignant.user.last_name,
            'email': enseignant.user.email,
        }
        form = EnseignantForm(instance=enseignant, initial=initial_data)
    
    return render(request, 'core/modifier_enseignant.html', {
        'form': form,
        'enseignant': enseignant
    })


@login_required
def supprimer_enseignant(request, pk):
    """Supprimer un enseignant"""
    enseignant = get_object_or_404(Enseignant, pk=pk)
    
    if request.method == 'POST':
        nom_complet = enseignant.user.get_full_name()
        enseignant.user.delete()  # Cela supprimera aussi l'enseignant par cascade
        messages.success(request, f'Enseignant {nom_complet} supprimé avec succès!')
        return redirect('enseignants_list')
    
    return render(request, 'core/supprimer_enseignant.html', {'enseignant': enseignant})


# Vues CRUD pour les Cours

@login_required
def ajouter_cours(request):
    """Ajouter un nouveau cours"""
    if request.method == 'POST':
        form = CoursForm(request.POST)
        if form.is_valid():
            cours = form.save()
            messages.success(request, f'Cours {cours.matiere.nom} ajouté avec succès!')
            return redirect('cours_list')
    else:
        form = CoursForm()
    
    return render(request, 'core/ajouter_cours.html', {'form': form})


@login_required
def modifier_cours(request, pk):
    """Modifier un cours"""
    cours = get_object_or_404(Cours, pk=pk)
    
    if request.method == 'POST':
        form = CoursForm(request.POST, instance=cours)
        if form.is_valid():
            form.save()
            messages.success(request, f'Cours {cours.matiere.nom} modifié avec succès!')
            return redirect('cours_list')
    else:
        form = CoursForm(instance=cours)
    
    return render(request, 'core/modifier_cours.html', {
        'form': form,
        'cours': cours
    })


@login_required
def supprimer_cours(request, pk):
    """Supprimer un cours"""
    cours = get_object_or_404(Cours, pk=pk)
    
    if request.method == 'POST':
        nom_cours = f"{cours.matiere.nom} - {cours.classe.nom}"
        cours.delete()
        messages.success(request, f'Cours {nom_cours} supprimé avec succès!')
        return redirect('cours_list')
    
    return render(request, 'core/supprimer_cours.html', {'cours': cours})


# Vues CRUD pour les Notes

@login_required
def ajouter_note(request):
    """Ajouter une nouvelle note"""
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save()
            messages.success(request, f'Note ajoutée pour {note.etudiant.user.get_full_name()}!')
            return redirect('notes_list')
    else:
        form = NoteForm()
    
    return render(request, 'core/ajouter_note.html', {'form': form})


@login_required
def modifier_note(request, pk):
    """Modifier une note"""
    note = get_object_or_404(Note, pk=pk)
    
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, f'Note modifiée pour {note.etudiant.user.get_full_name()}!')
            return redirect('notes_list')
    else:
        form = NoteForm(instance=note)
    
    return render(request, 'core/modifier_note.html', {
        'form': form,
        'note': note
    })


@login_required
def supprimer_note(request, pk):
    """Supprimer une note"""
    note = get_object_or_404(Note, pk=pk)
    
    if request.method == 'POST':
        etudiant_nom = note.etudiant.user.get_full_name()
        note.delete()
        messages.success(request, f'Note supprimée pour {etudiant_nom}!')
        return redirect('notes_list')
    
    return render(request, 'core/supprimer_note.html', {'note': note})


# Vues pour la gestion avancée des utilisateurs

@login_required
def modifier_utilisateur(request, user_id):
    """Modifier un utilisateur (admin uniquement)"""
    if not request.user.is_superuser:
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        # Mettre à jour les informations de base
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.is_active = request.POST.get('is_active') == 'on'
        user.save()
        
        # Mettre à jour le profil
        if hasattr(user, 'profil') and user.profil:
            user.profil.telephone = request.POST.get('telephone', '')
            user.profil.save()
        
        messages.success(request, f'Utilisateur {user.get_full_name()} modifié avec succès!')
        return redirect('gestion_utilisateurs')
    
    return render(request, 'core/modifier_utilisateur.html', {'user_obj': user})


@login_required
def reinitialiser_mot_de_passe(request, user_id):
    """Réinitialiser le mot de passe d'un utilisateur (admin uniquement)"""
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Accès non autorisé'})
    
    if request.method == 'POST':
        try:
            user = get_object_or_404(User, id=user_id)
            
            # Générer un nouveau mot de passe temporaire
            nouveau_mot_de_passe = generer_mot_de_passe()
            user.set_password(nouveau_mot_de_passe)
            user.save()
            
            # Marquer comme mot de passe temporaire
            if hasattr(user, 'profil') and user.profil:
                user.profil.mot_de_passe_temporaire = True
                user.profil.save()
            else:
                creer_profil_utilisateur(user)
                user.profil.mot_de_passe_temporaire = True
                user.profil.save()
            
            # Envoyer notification
            envoyer_notification(
                user,
                'info',
                'Mot de passe réinitialisé',
                f'Votre nouveau mot de passe temporaire est : {nouveau_mot_de_passe}'
            )
            
            # Envoyer email si possible
            try:
                envoyer_email_bienvenue(user, nouveau_mot_de_passe)
            except:
                pass  # Email optionnel
            
            return JsonResponse({
                'success': True, 
                'message': f'Mot de passe réinitialisé. Nouveau mot de passe : {nouveau_mot_de_passe}'
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})


@login_required
def toggle_utilisateur(request, user_id):
    """Activer/Désactiver un utilisateur (admin uniquement)"""
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Accès non autorisé'})
    
    if request.method == 'POST':
        try:
            user = get_object_or_404(User, id=user_id)
            
            # Ne pas désactiver les superusers
            if user.is_superuser:
                return JsonResponse({'success': False, 'error': 'Impossible de désactiver un administrateur'})
            
            # Inverser le statut
            user.is_active = not user.is_active
            user.save()
            
            # Mettre à jour le profil
            if hasattr(user, 'profil') and user.profil:
                user.profil.compte_active = user.is_active
                user.profil.save()
            
            statut = "activé" if user.is_active else "désactivé"
            
            # Envoyer notification
            envoyer_notification(
                user,
                'warning' if not user.is_active else 'success',
                f'Compte {statut}',
                f'Votre compte a été {statut} par un administrateur.'
            )
            
            return JsonResponse({
                'success': True, 
                'message': f'Utilisateur {user.get_full_name()} {statut} avec succès',
                'new_status': user.is_active
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})


@login_required
def get_user_password(request, user_id):
    """Récupérer le mot de passe d'un utilisateur (admin uniquement)"""
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Accès non autorisé'})
    
    try:
        user = get_object_or_404(User, id=user_id)
        
        # Vérifier si l'utilisateur a un profil avec le dernier mot de passe stocké
        if hasattr(user, 'profil') and user.profil and user.profil.dernier_mot_de_passe:
            # Afficher le vrai dernier mot de passe défini
            display_password = user.profil.dernier_mot_de_passe
            note = "Dernier mot de passe défini"
        else:
            # Sinon, afficher le mot de passe par défaut selon le type
            if user.is_superuser:
                display_password = "admin123"
            elif hasattr(user, 'enseignant'):
                display_password = "prof123"
            elif hasattr(user, 'etudiant'):
                display_password = "etudiant123"
            else:
                display_password = "user123"
            note = "Mot de passe par défaut (peut avoir été modifié)"
            
        return JsonResponse({
            'success': True, 
            'password': display_password,
            'note': note,
            'username': user.username,
            'has_temp_password': hasattr(user, 'profil') and user.profil and user.profil.mot_de_passe_temporaire if hasattr(user, 'profil') and user.profil else False
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def set_user_password(request, user_id):
    """Définir un nouveau mot de passe pour un utilisateur (admin uniquement)"""
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Accès non autorisé'})
    
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            new_password = data.get('new_password')
            
            print(f"DEBUG: Tentative de changement de mot de passe pour utilisateur {user_id}")
            print(f"DEBUG: Nouveau mot de passe reçu: {new_password}")
            
            if not new_password or len(new_password) < 8:
                return JsonResponse({'success': False, 'error': 'Le mot de passe doit contenir au moins 8 caractères'})
            
            user = get_object_or_404(User, id=user_id)
            print(f"DEBUG: Utilisateur trouvé: {user.username}")
            
            # Changer le mot de passe
            user.set_password(new_password)
            user.save()
            print(f"DEBUG: Mot de passe changé et sauvegardé pour {user.username}")
            
            # Marquer comme mot de passe non temporaire et stocker le nouveau mot de passe
            if hasattr(user, 'profil') and user.profil:
                user.profil.mot_de_passe_temporaire = False
                user.profil.dernier_mot_de_passe = new_password  # Stocker le nouveau mot de passe
                user.profil.save()
                print(f"DEBUG: Profil mis à jour - mot de passe non temporaire")
            else:
                # Créer le profil s'il n'existe pas
                creer_profil_utilisateur(user)
                user.profil.mot_de_passe_temporaire = False
                user.profil.dernier_mot_de_passe = new_password  # Stocker le nouveau mot de passe
                user.profil.save()
                print(f"DEBUG: Profil créé pour {user.username}")
            
            # Envoyer notification
            try:
                envoyer_notification(
                    user,
                    'info',
                    'Mot de passe modifié',
                    'Votre mot de passe a été modifié par un administrateur.'
                )
                print(f"DEBUG: Notification envoyée")
            except Exception as notif_error:
                print(f"DEBUG: Erreur notification: {notif_error}")
            
            return JsonResponse({
                'success': True, 
                'message': f'Mot de passe modifié pour {user.get_full_name()}',
                'debug': f'Mot de passe changé avec succès pour {user.username}'
            })
            
        except Exception as e:
            print(f"DEBUG: Erreur dans set_user_password: {str(e)}")
            return JsonResponse({'success': False, 'error': f'Erreur: {str(e)}'})
    
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})


# Vues pour l'emploi du temps

@login_required
def emploi_du_temps_list(request):
    """Liste des emplois du temps"""
    emplois = EmploiDuTemps.objects.select_related('cours', 'cours__matiere', 'cours__enseignant', 'cours__classe').all()
    
    # Filtres
    classe_id = request.GET.get('classe')
    enseignant_id = request.GET.get('enseignant')
    jour = request.GET.get('jour')
    
    if classe_id:
        emplois = emplois.filter(cours__classe_id=classe_id)
    if enseignant_id:
        emplois = emplois.filter(cours__enseignant_id=enseignant_id)
    if jour:
        emplois = emplois.filter(jour=jour)
    
    # Organiser par jour et heure
    emplois = emplois.order_by('jour', 'heure_debut')
    
    context = {
        'emplois': emplois,
        'classes': Classe.objects.all(),
        'enseignants': Enseignant.objects.all(),
        'jours': EmploiDuTemps.JOURS_CHOICES,
    }
    
    return render(request, 'core/emploi_du_temps_list.html', context)


@login_required
def ajouter_emploi_du_temps(request):
    """Ajouter un emploi du temps (admin/enseignant uniquement)"""
    if not (request.user.is_superuser or hasattr(request.user, 'enseignant')):
        messages.error(request, 'Accès non autorisé.')
        return redirect('emploi_du_temps_list')
        
    if request.method == 'POST':
        try:
            cours_id = request.POST.get('cours')
            jour = request.POST.get('jour')
            heure_debut = request.POST.get('heure_debut')
            heure_fin = request.POST.get('heure_fin')
            type_cours = request.POST.get('type_cours')
            salle = request.POST.get('salle')
            
            cours = get_object_or_404(Cours, id=cours_id)
            
            # Vérifier les conflits d'horaires
            conflits = EmploiDuTemps.objects.filter(
                jour=jour,
                heure_debut__lt=heure_fin,
                heure_fin__gt=heure_debut
            ).filter(
                Q(salle=salle) | Q(cours__enseignant=cours.enseignant) | Q(cours__classe=cours.classe)
            )
            
            if conflits.exists():
                messages.error(request, 'Conflit d\'horaire détecté (salle, enseignant ou classe déjà occupé).')
            else:
                EmploiDuTemps.objects.create(
                    cours=cours,
                    jour=jour,
                    heure_debut=heure_debut,
                    heure_fin=heure_fin,
                    type_cours=type_cours,
                    salle=salle
                )
                messages.success(request, 'Emploi du temps ajouté avec succès!')
                return redirect('emploi_du_temps_list')
                
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'ajout: {str(e)}')
    
    context = {
        'cours_list': Cours.objects.all(),
        'jours': EmploiDuTemps.JOURS_CHOICES,
        'types_cours': EmploiDuTemps.TYPE_COURS_CHOICES,
    }
    
    return render(request, 'core/ajouter_emploi_du_temps.html', context)


@login_required
def modifier_emploi_du_temps(request, pk):
    """Modifier un emploi du temps"""
    emploi = get_object_or_404(EmploiDuTemps, pk=pk)
    
    if not (request.user.is_superuser or (hasattr(request.user, 'enseignant') and request.user.enseignant == emploi.cours.enseignant)):
        messages.error(request, 'Accès non autorisé.')
        return redirect('emploi_du_temps_list')
    
    if request.method == 'POST':
        try:
            cours_id = request.POST.get('cours')
            jour = request.POST.get('jour')
            heure_debut = request.POST.get('heure_debut')
            heure_fin = request.POST.get('heure_fin')
            type_cours = request.POST.get('type_cours')
            salle = request.POST.get('salle')
            
            cours = get_object_or_404(Cours, id=cours_id)
            
            # Vérifier les conflits (exclure l'emploi actuel)
            conflits = EmploiDuTemps.objects.filter(
                jour=jour,
                heure_debut__lt=heure_fin,
                heure_fin__gt=heure_debut
            ).filter(
                Q(salle=salle) | Q(cours__enseignant=cours.enseignant) | Q(cours__classe=cours.classe)
            ).exclude(pk=pk)
            
            if conflits.exists():
                messages.error(request, 'Conflit d\'horaire détecté.')
            else:
                emploi.cours = cours
                emploi.jour = jour
                emploi.heure_debut = heure_debut
                emploi.heure_fin = heure_fin
                emploi.type_cours = type_cours
                emploi.salle = salle
                emploi.save()
                
                messages.success(request, 'Emploi du temps modifié avec succès!')
                return redirect('emploi_du_temps_list')
                
        except Exception as e:
            messages.error(request, f'Erreur lors de la modification: {str(e)}')
    
    context = {
        'emploi': emploi,
        'cours_list': Cours.objects.all(),
        'jours': EmploiDuTemps.JOURS_CHOICES,
        'types_cours': EmploiDuTemps.TYPE_COURS_CHOICES,
    }
    
    return render(request, 'core/modifier_emploi_du_temps.html', context)


@login_required
def supprimer_emploi_du_temps(request, pk):
    """Supprimer un emploi du temps"""
    emploi = get_object_or_404(EmploiDuTemps, pk=pk)
    
    if not (request.user.is_superuser or (hasattr(request.user, 'enseignant') and request.user.enseignant == emploi.cours.enseignant)):
        messages.error(request, 'Accès non autorisé.')
        return redirect('emploi_du_temps_list')
    
    if request.method == 'POST':
        emploi_info = f"{emploi.cours.matiere.nom} - {emploi.get_jour_display()} {emploi.heure_debut}-{emploi.heure_fin}"
        emploi.delete()
        messages.success(request, f'Emploi du temps "{emploi_info}" supprimé avec succès!')
        return redirect('emploi_du_temps_list')
    
    return render(request, 'core/supprimer_emploi_du_temps.html', {'emploi': emploi})


@login_required
def comptes_test(request):
    """Afficher les comptes de test disponibles (admin uniquement)"""
    if not request.user.is_superuser:
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    enseignants = Enseignant.objects.select_related('user', 'departement').all()[:5]
    etudiants = Etudiant.objects.select_related('user', 'classe').all()[:10]
    
    context = {
        'enseignants': enseignants,
        'etudiants': etudiants,
    }
    
    return render(request, 'core/comptes_test.html', context)


@login_required
@require_POST
def reinitialiser_mot_de_passe_utilisateur(request, user_id):
    """Réinitialiser le mot de passe d'un utilisateur spécifique (admin uniquement)"""
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'message': 'Accès non autorisé.'})
    
    try:
        user = get_object_or_404(User, id=user_id)
        nouveau_mot_de_passe = 'password123'
        user.set_password(nouveau_mot_de_passe)
        user.save()
        
        return JsonResponse({
            'success': True, 
            'message': f'Mot de passe de {user.username} réinitialisé avec succès.',
            'nouveau_mot_de_passe': nouveau_mot_de_passe
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Erreur: {str(e)}'})


@login_required
@require_POST
def reinitialiser_tous_mots_de_passe(request):
    """Réinitialiser tous les mots de passe (admin uniquement)"""
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'message': 'Accès non autorisé.'})
    
    try:
        # Réinitialiser les étudiants
        etudiants = User.objects.filter(etudiant__isnull=False)
        for user in etudiants:
            user.set_password('password123')
            user.save()
        
        # Réinitialiser les enseignants
        enseignants = User.objects.filter(enseignant__isnull=False)
        for user in enseignants:
            user.set_password('password123')
            user.save()
        
        # Garder admin123 pour l'admin
        try:
            admin = User.objects.get(username='admin')
            admin.set_password('admin123')
            admin.save()
        except User.DoesNotExist:
            pass
        
        total_users = etudiants.count() + enseignants.count()
        
        return JsonResponse({
            'success': True, 
            'message': f'{total_users} mots de passe réinitialisés avec succès.',
            'details': {
                'etudiants': etudiants.count(),
                'enseignants': enseignants.count()
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Erreur: {str(e)}'})


@login_required
def generer_mot_de_passe_aleatoire(request, user_id):
    """Générer un mot de passe aléatoire pour un utilisateur (admin uniquement)"""
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'message': 'Accès non autorisé.'})
    
    try:
        import random
        import string
        
        user = get_object_or_404(User, id=user_id)
        
        # Générer un mot de passe aléatoire de 8 caractères
        caracteres = string.ascii_letters + string.digits
        nouveau_mot_de_passe = ''.join(random.choice(caracteres) for _ in range(8))
        
        user.set_password(nouveau_mot_de_passe)
        user.save()
        
        return JsonResponse({
            'success': True, 
            'message': f'Nouveau mot de passe généré pour {user.username}.',
            'nouveau_mot_de_passe': nouveau_mot_de_passe
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Erreur: {str(e)}'})
