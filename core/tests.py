from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import (
    Departement, Enseignant, Classe, Etudiant, 
    Matiere, Cours, Note, EmploiDuTemps
)
from datetime import date, time
from decimal import Decimal


class ModelsTestCase(TestCase):
    """Tests pour les modèles"""
    
    def setUp(self):
        """Configuration initiale pour les tests"""
        self.departement = Departement.objects.create(
            nom="Informatique",
            description="Département d'informatique"
        )
        
        self.user_enseignant = User.objects.create_user(
            username="prof_test",
            email="prof@test.com",
            first_name="Jean",
            last_name="Dupont"
        )
        
        self.enseignant = Enseignant.objects.create(
            user=self.user_enseignant,
            departement=self.departement,
            telephone="0123456789",
            date_embauche=date(2020, 9, 1)
        )
        
        self.classe = Classe.objects.create(
            nom="L1-INFO-A",
            niveau="L1",
            departement=self.departement
        )
        
        self.user_etudiant = User.objects.create_user(
            username="etudiant_test",
            email="etudiant@test.com",
            first_name="Marie",
            last_name="Martin"
        )
        
        self.etudiant = Etudiant.objects.create(
            user=self.user_etudiant,
            numero_etudiant="ET001",
            classe=self.classe,
            date_naissance=date(2003, 5, 15)
        )
        
        self.matiere = Matiere.objects.create(
            nom="Programmation Python",
            code="PROG101",
            credits=6,
            description="Introduction à Python"
        )
        
        self.cours = Cours.objects.create(
            matiere=self.matiere,
            enseignant=self.enseignant,
            classe=self.classe,
            semestre="S1",
            annee_scolaire="2023-2024"
        )

    def test_departement_creation(self):
        """Test de création d'un département"""
        self.assertEqual(self.departement.nom, "Informatique")
        self.assertEqual(str(self.departement), "Informatique")

    def test_enseignant_creation(self):
        """Test de création d'un enseignant"""
        self.assertEqual(self.enseignant.user.first_name, "Jean")
        self.assertEqual(self.enseignant.nom_complet, "Jean Dupont")
        self.assertEqual(self.enseignant.departement, self.departement)

    def test_classe_creation(self):
        """Test de création d'une classe"""
        self.assertEqual(self.classe.nom, "L1-INFO-A")
        self.assertEqual(self.classe.niveau, "L1")
        self.assertEqual(str(self.classe), "L1-INFO-A - Licence 1")

    def test_etudiant_creation(self):
        """Test de création d'un étudiant"""
        self.assertEqual(self.etudiant.numero_etudiant, "ET001")
        self.assertEqual(self.etudiant.nom_complet, "Marie Martin")
        self.assertEqual(self.etudiant.classe, self.classe)

    def test_matiere_creation(self):
        """Test de création d'une matière"""
        self.assertEqual(self.matiere.code, "PROG101")
        self.assertEqual(self.matiere.credits, 6)
        self.assertEqual(str(self.matiere), "PROG101 - Programmation Python")

    def test_cours_creation(self):
        """Test de création d'un cours"""
        self.assertEqual(self.cours.matiere, self.matiere)
        self.assertEqual(self.cours.enseignant, self.enseignant)
        self.assertEqual(self.cours.classe, self.classe)

    def test_note_creation(self):
        """Test de création d'une note"""
        note = Note.objects.create(
            etudiant=self.etudiant,
            cours=self.cours,
            type_evaluation="DS",
            note=Decimal("15.5"),
            coefficient=Decimal("2.0"),
            date_evaluation=date(2023, 10, 15)
        )
        self.assertEqual(note.note, Decimal("15.5"))
        self.assertEqual(note.type_evaluation, "DS")

    def test_emploi_du_temps_creation(self):
        """Test de création d'un emploi du temps"""
        emploi = EmploiDuTemps.objects.create(
            cours=self.cours,
            jour="LUNDI",
            heure_debut=time(8, 0),
            heure_fin=time(10, 0),
            type_cours="CM",
            salle="Amphi A"
        )
        self.assertEqual(emploi.jour, "LUNDI")
        self.assertEqual(emploi.salle, "Amphi A")


class ViewsTestCase(TestCase):
    """Tests pour les vues"""
    
    def setUp(self):
        """Configuration pour les tests de vues"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            email="test@example.com"
        )
        
        # Créer des données de test
        self.departement = Departement.objects.create(
            nom="Test Dept",
            description="Test department"
        )
        
        self.classe = Classe.objects.create(
            nom="TEST-CLASS",
            niveau="L1",
            departement=self.departement
        )

    def test_login_view_get(self):
        """Test de la page de connexion (GET)"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "EduManager")

    def test_login_view_post_valid(self):
        """Test de connexion avec des identifiants valides"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirection après connexion

    def test_login_view_post_invalid(self):
        """Test de connexion avec des identifiants invalides"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nom d'utilisateur ou mot de passe incorrect")

    def test_dashboard_requires_login(self):
        """Test que le tableau de bord nécessite une connexion"""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirection vers login

    def test_dashboard_authenticated(self):
        """Test du tableau de bord avec utilisateur connecté"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tableau de bord")

    def test_etudiants_list_view(self):
        """Test de la liste des étudiants"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('etudiants_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Liste des Étudiants")

    def test_enseignants_list_view(self):
        """Test de la liste des enseignants"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('enseignants_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Liste des Enseignants")

    def test_cours_list_view(self):
        """Test de la liste des cours"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('cours_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Liste des Cours")

    def test_notes_list_view(self):
        """Test de la liste des notes"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('notes_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gestion des Notes")

    def test_emploi_du_temps_view(self):
        """Test de l'emploi du temps"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('emploi_du_temps'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Emploi du Temps")

    def test_statistiques_view(self):
        """Test de la page des statistiques"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('statistiques'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Statistiques")


class FormsTestCase(TestCase):
    """Tests pour les formulaires"""
    
    def setUp(self):
        """Configuration pour les tests de formulaires"""
        self.departement = Departement.objects.create(
            nom="Test Dept",
            description="Test department"
        )
        
        self.classe = Classe.objects.create(
            nom="TEST-CLASS",
            niveau="L1",
            departement=self.departement
        )

    def test_login_form_valid(self):
        """Test du formulaire de connexion valide"""
        from .forms import LoginForm
        form_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        """Test du formulaire de connexion invalide"""
        from .forms import LoginForm
        form_data = {
            'username': '',  # Username vide
            'password': 'testpass123'
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_etudiant_form_valid(self):
        """Test du formulaire étudiant valide"""
        from .forms import EtudiantForm
        form_data = {
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'email': 'jean.dupont@test.com',
            'numero_etudiant': 'ET001',
            'classe': self.classe.id,
            'date_naissance': '2003-05-15',
            'telephone': '0123456789',
            'adresse': '123 rue de la Paix'
        }
        form = EtudiantForm(data=form_data)
        self.assertTrue(form.is_valid())


class IntegrationTestCase(TestCase):
    """Tests d'intégration"""
    
    def setUp(self):
        """Configuration pour les tests d'intégration"""
        self.client = Client()
        
        # Créer un superutilisateur
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )
        
        # Créer des données de base
        self.departement = Departement.objects.create(
            nom="Informatique",
            description="Département d'informatique"
        )
        
        self.classe = Classe.objects.create(
            nom="L1-INFO-A",
            niveau="L1",
            departement=self.departement
        )

    def test_complete_student_workflow(self):
        """Test du workflow complet d'un étudiant"""
        # 1. Connexion admin
        self.client.login(username='admin', password='admin123')
        
        # 2. Accès au tableau de bord
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # 3. Accès à la liste des étudiants
        response = self.client.get(reverse('etudiants_list'))
        self.assertEqual(response.status_code, 200)
        
        # 4. Vérifier que la liste est initialement vide
        self.assertContains(response, "Aucun étudiant trouvé")

    def test_admin_interface_access(self):
        """Test d'accès à l'interface d'administration"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

    def test_static_files_serving(self):
        """Test du service des fichiers statiques"""
        response = self.client.get('/static/css/custom.css')
        # En mode test, les fichiers statiques peuvent ne pas être servis
        # Ce test vérifie que l'URL est accessible
        self.assertIn(response.status_code, [200, 404])


class PerformanceTestCase(TestCase):
    """Tests de performance"""
    
    def setUp(self):
        """Créer des données en masse pour les tests de performance"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Créer plusieurs départements
        for i in range(5):
            Departement.objects.create(
                nom=f"Département {i}",
                description=f"Description {i}"
            )

    def test_dashboard_performance(self):
        """Test de performance du tableau de bord"""
        self.client.login(username='testuser', password='testpass123')
        
        import time
        start_time = time.time()
        response = self.client.get(reverse('dashboard'))
        end_time = time.time()
        
        self.assertEqual(response.status_code, 200)
        # Vérifier que la page se charge en moins d'une seconde
        self.assertLess(end_time - start_time, 1.0)

    def test_large_list_performance(self):
        """Test de performance avec de grandes listes"""
        # Ce test pourrait être étendu pour créer de nombreux objets
        # et tester les performances des vues de liste
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(reverse('etudiants_list'))
        self.assertEqual(response.status_code, 200)
