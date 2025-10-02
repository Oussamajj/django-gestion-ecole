from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import (
    Departement, Enseignant, Classe, Etudiant, 
    Matiere, Cours, Note, EmploiDuTemps
)
from datetime import date, time
import random


class Command(BaseCommand):
    help = 'Créer des données d\'exemple pour tester l\'application'

    def handle(self, *args, **options):
        self.stdout.write('Création des données d\'exemple...')
        
        # Créer les départements
        dept_info = Departement.objects.get_or_create(
            nom='Informatique',
            description='Département d\'informatique et sciences du numérique'
        )[0]
        
        dept_math = Departement.objects.get_or_create(
            nom='Mathématiques',
            description='Département de mathématiques appliquées'
        )[0]
        
        dept_phys = Departement.objects.get_or_create(
            nom='Physique',
            description='Département de physique et sciences physiques'
        )[0]
        
        # Créer les classes
        classes_data = [
            ('L1-INFO-A', 'L1', dept_info),
            ('L1-INFO-B', 'L1', dept_info),
            ('L2-INFO-A', 'L2', dept_info),
            ('L3-INFO-A', 'L3', dept_info),
            ('M1-INFO', 'M1', dept_info),
            ('L1-MATH-A', 'L1', dept_math),
            ('L2-MATH-A', 'L2', dept_math),
            ('L1-PHYS-A', 'L1', dept_phys),
        ]
        
        classes = {}
        for nom, niveau, dept in classes_data:
            classe = Classe.objects.get_or_create(
                nom=nom,
                niveau=niveau,
                departement=dept
            )[0]
            classes[nom] = classe
        
        # Créer les enseignants
        enseignants_data = [
            ('Martin', 'Dupont', 'martin.dupont@universite.fr', dept_info, '2020-09-01'),
            ('Sophie', 'Bernard', 'sophie.bernard@universite.fr', dept_info, '2018-09-01'),
            ('Jean', 'Moreau', 'jean.moreau@universite.fr', dept_math, '2015-09-01'),
            ('Marie', 'Dubois', 'marie.dubois@universite.fr', dept_phys, '2019-09-01'),
            ('Pierre', 'Leroy', 'pierre.leroy@universite.fr', dept_info, '2021-09-01'),
        ]
        
        enseignants = {}
        for prenom, nom, email, dept, date_embauche in enseignants_data:
            user = User.objects.get_or_create(
                username=f'{prenom.lower()}.{nom.lower()}',
                defaults={
                    'first_name': prenom,
                    'last_name': nom,
                    'email': email,
                    'is_staff': True
                }
            )[0]
            
            # Définir le mot de passe pour les nouveaux utilisateurs
            if not user.has_usable_password():
                user.set_password('password123')
                user.save()
            
            if not hasattr(user, 'enseignant'):
                enseignant = Enseignant.objects.create(
                    user=user,
                    departement=dept,
                    telephone=f'0{random.randint(100000000, 999999999)}',
                    date_embauche=date_embauche,
                    adresse=f'{random.randint(1, 100)} rue de la République, {random.randint(10000, 99999)} Ville'
                )
                enseignants[f'{prenom} {nom}'] = enseignant
        
        # Créer les étudiants
        etudiants_data = [
            ('Alice', 'Martin', 'alice.martin@etudiant.fr', 'ET001', classes['L1-INFO-A'], '2003-05-15'),
            ('Bob', 'Durand', 'bob.durand@etudiant.fr', 'ET002', classes['L1-INFO-A'], '2003-08-22'),
            ('Claire', 'Petit', 'claire.petit@etudiant.fr', 'ET003', classes['L1-INFO-B'], '2003-03-10'),
            ('David', 'Roux', 'david.roux@etudiant.fr', 'ET004', classes['L2-INFO-A'], '2002-11-30'),
            ('Emma', 'Blanc', 'emma.blanc@etudiant.fr', 'ET005', classes['L3-INFO-A'], '2001-07-18'),
            ('Felix', 'Noir', 'felix.noir@etudiant.fr', 'ET006', classes['M1-INFO'], '2000-12-05'),
            ('Grace', 'Vert', 'grace.vert@etudiant.fr', 'ET007', classes['L1-MATH-A'], '2003-09-12'),
            ('Hugo', 'Bleu', 'hugo.bleu@etudiant.fr', 'ET008', classes['L2-MATH-A'], '2002-04-25'),
            ('Iris', 'Rose', 'iris.rose@etudiant.fr', 'ET009', classes['L1-PHYS-A'], '2003-01-08'),
            ('Jules', 'Orange', 'jules.orange@etudiant.fr', 'ET010', classes['L1-INFO-A'], '2003-06-14'),
        ]
        
        etudiants = {}
        for prenom, nom, email, numero, classe, naissance in etudiants_data:
            user = User.objects.get_or_create(
                username=numero.lower(),
                defaults={
                    'first_name': prenom,
                    'last_name': nom,
                    'email': email
                }
            )[0]
            
            # Définir le mot de passe pour les nouveaux utilisateurs
            if not user.has_usable_password():
                user.set_password('password123')
                user.save()
            
            if not hasattr(user, 'etudiant'):
                etudiant = Etudiant.objects.create(
                    user=user,
                    numero_etudiant=numero,
                    classe=classe,
                    date_naissance=naissance,
                    telephone=f'0{random.randint(600000000, 799999999)}',
                    adresse=f'{random.randint(1, 200)} avenue des Étudiants, {random.randint(10000, 99999)} Ville'
                )
                etudiants[f'{prenom} {nom}'] = etudiant
        
        # Créer les matières
        matieres_data = [
            ('Programmation Python', 'PROG101', 6, 'Introduction à la programmation en Python'),
            ('Mathématiques Discrètes', 'MATH101', 6, 'Logique, ensembles, graphes'),
            ('Base de Données', 'BDD101', 4, 'Conception et gestion de bases de données'),
            ('Algorithmique', 'ALGO101', 6, 'Algorithmes et structures de données'),
            ('Physique Générale', 'PHYS101', 6, 'Mécanique et thermodynamique'),
            ('Analyse Mathématique', 'MATH201', 6, 'Fonctions, dérivées, intégrales'),
            ('Programmation Web', 'WEB101', 4, 'HTML, CSS, JavaScript'),
            ('Systèmes d\'Exploitation', 'SYS101', 6, 'Concepts des systèmes d\'exploitation'),
        ]
        
        matieres = {}
        for nom, code, credits, description in matieres_data:
            matiere = Matiere.objects.get_or_create(
                code=code,
                defaults={
                    'nom': nom,
                    'credits': credits,
                    'description': description
                }
            )[0]
            matieres[code] = matiere
        
        # Créer les cours
        cours_data = [
            (matieres['PROG101'], list(enseignants.values())[0], classes['L1-INFO-A'], 'S1', '2023-2024'),
            (matieres['MATH101'], list(enseignants.values())[2], classes['L1-INFO-A'], 'S1', '2023-2024'),
            (matieres['ALGO101'], list(enseignants.values())[1], classes['L2-INFO-A'], 'S1', '2023-2024'),
            (matieres['BDD101'], list(enseignants.values())[0], classes['L2-INFO-A'], 'S2', '2023-2024'),
            (matieres['WEB101'], list(enseignants.values())[4], classes['L3-INFO-A'], 'S1', '2023-2024'),
            (matieres['SYS101'], list(enseignants.values())[1], classes['L3-INFO-A'], 'S2', '2023-2024'),
            (matieres['PHYS101'], list(enseignants.values())[3], classes['L1-PHYS-A'], 'S1', '2023-2024'),
            (matieres['MATH201'], list(enseignants.values())[2], classes['L1-MATH-A'], 'S1', '2023-2024'),
        ]
        
        cours_list = []
        for matiere, enseignant, classe, semestre, annee in cours_data:
            cours = Cours.objects.get_or_create(
                matiere=matiere,
                enseignant=enseignant,
                classe=classe,
                semestre=semestre,
                annee_scolaire=annee
            )[0]
            cours_list.append(cours)
        
        # Créer des notes d'exemple
        types_eval = ['DS', 'CC', 'TP', 'PROJET', 'EXAMEN']
        
        for cours in cours_list:
            etudiants_classe = Etudiant.objects.filter(classe=cours.classe)
            for etudiant in etudiants_classe:
                # Créer 3-5 notes par étudiant par cours
                nb_notes = random.randint(3, 5)
                for i in range(nb_notes):
                    note_value = round(random.uniform(8, 18), 1)  # Notes entre 8 et 18
                    Note.objects.get_or_create(
                        etudiant=etudiant,
                        cours=cours,
                        type_evaluation=random.choice(types_eval),
                        note=note_value,
                        coefficient=random.choice([1.0, 1.5, 2.0]),
                        date_evaluation=date(2023, random.randint(10, 12), random.randint(1, 28)),
                        commentaire=f'Évaluation {i+1} - {"Bon travail" if note_value >= 12 else "Peut mieux faire"}'
                    )
        
        # Créer un emploi du temps d'exemple
        emploi_data = [
            (cours_list[0], 'LUNDI', time(8, 0), time(10, 0), 'CM', 'Amphi A'),
            (cours_list[1], 'LUNDI', time(10, 15), time(12, 15), 'CM', 'Amphi B'),
            (cours_list[0], 'MARDI', time(14, 0), time(16, 0), 'TD', 'Salle 101'),
            (cours_list[2], 'MERCREDI', time(8, 0), time(10, 0), 'CM', 'Amphi C'),
            (cours_list[3], 'JEUDI', time(14, 0), time(17, 0), 'TP', 'Lab Info 1'),
            (cours_list[4], 'VENDREDI', time(9, 0), time(12, 0), 'TP', 'Lab Info 2'),
        ]
        
        for cours, jour, debut, fin, type_cours, salle in emploi_data:
            EmploiDuTemps.objects.get_or_create(
                cours=cours,
                jour=jour,
                heure_debut=debut,
                heure_fin=fin,
                type_cours=type_cours,
                salle=salle
            )
        
        # Créer un utilisateur admin par défaut
        admin_user = User.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'Admin',
                'last_name': 'System',
                'email': 'admin@edumanager.com',
                'is_staff': True,
                'is_superuser': True
            }
        )[0]
        admin_user.set_password('admin123')
        admin_user.save()
        
        self.stdout.write(
            self.style.SUCCESS('Données d\'exemple créées avec succès!')
        )
        self.stdout.write('Comptes créés:')
        self.stdout.write('- Admin: admin / admin123')
        self.stdout.write('- Enseignants: martin.dupont / password123 (etc.)')
        self.stdout.write('- Étudiants: et001 / password123 (etc.)')
        self.stdout.write('\nUtilisez "python manage.py changepassword <username>" pour changer les mots de passe.')
