#!/usr/bin/env python
"""
Script de vérification du projet EduManager
Vérifie que tous les fichiers nécessaires sont présents et correctement configurés
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description=""):
    """Vérifier qu'un fichier existe"""
    if os.path.exists(filepath):
        print(f"✅ {filepath} - {description}")
        return True
    else:
        print(f"❌ {filepath} - MANQUANT - {description}")
        return False

def check_directory_exists(dirpath, description=""):
    """Vérifier qu'un répertoire existe"""
    if os.path.isdir(dirpath):
        print(f"✅ {dirpath}/ - {description}")
        return True
    else:
        print(f"❌ {dirpath}/ - MANQUANT - {description}")
        return False

def check_file_content(filepath, content_check, description=""):
    """Vérifier le contenu d'un fichier"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if content_check in content:
                print(f"✅ {filepath} - {description}")
                return True
            else:
                print(f"⚠️  {filepath} - {description} - Contenu à vérifier")
                return False
    except Exception as e:
        print(f"❌ {filepath} - Erreur de lecture: {e}")
        return False

def main():
    """Fonction principale de vérification"""
    print("🔍 EduManager - Vérification du projet")
    print("=" * 50)
    
    errors = 0
    warnings = 0
    
    # Vérification des fichiers principaux
    print("\n📁 Fichiers principaux:")
    files_to_check = [
        ("manage.py", "Script de gestion Django"),
        ("requirements.txt", "Dépendances Python"),
        ("README.md", "Documentation principale"),
        ("CHANGELOG.md", "Journal des modifications"),
        (".gitignore", "Fichiers à ignorer par Git"),
        (".env.example", "Exemple de configuration"),
        ("Dockerfile", "Configuration Docker"),
        ("docker-compose.yml", "Orchestration Docker"),
        ("nginx.conf", "Configuration Nginx"),
        ("run_server.py", "Script de lancement"),
        ("check_project.py", "Script de vérification"),
    ]
    
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            errors += 1
    
    # Vérification des répertoires
    print("\n📂 Structure des répertoires:")
    directories_to_check = [
        ("school_management", "Configuration Django"),
        ("core", "Application principale"),
        ("templates", "Templates HTML"),
        ("static", "Fichiers statiques"),
        ("media", "Fichiers uploadés"),
        ("core/migrations", "Migrations Django"),
        ("core/management", "Commandes personnalisées"),
        ("core/management/commands", "Scripts de gestion"),
    ]
    
    for dirpath, description in directories_to_check:
        if not check_directory_exists(dirpath, description):
            errors += 1
    
    # Vérification des fichiers de configuration Django
    print("\n⚙️  Configuration Django:")
    django_files = [
        ("school_management/__init__.py", "Module Python"),
        ("school_management/settings.py", "Configuration Django"),
        ("school_management/urls.py", "URLs principales"),
        ("school_management/wsgi.py", "Configuration WSGI"),
        ("school_management/asgi.py", "Configuration ASGI"),
    ]
    
    for filepath, description in django_files:
        if not check_file_exists(filepath, description):
            errors += 1
    
    # Vérification de l'application core
    print("\n🎯 Application Core:")
    core_files = [
        ("core/__init__.py", "Module Python"),
        ("core/models.py", "Modèles de données"),
        ("core/views.py", "Vues Django"),
        ("core/urls.py", "URLs de l'application"),
        ("core/forms.py", "Formulaires Django"),
        ("core/admin.py", "Interface d'administration"),
        ("core/apps.py", "Configuration de l'application"),
        ("core/tests.py", "Tests unitaires"),
        ("core/migrations/__init__.py", "Module migrations"),
        ("core/management/__init__.py", "Module management"),
        ("core/management/commands/__init__.py", "Module commands"),
        ("core/management/commands/create_sample_data.py", "Commande de données d'exemple"),
    ]
    
    for filepath, description in core_files:
        if not check_file_exists(filepath, description):
            errors += 1
    
    # Vérification des templates
    print("\n🎨 Templates HTML:")
    template_files = [
        ("templates/base.html", "Template de base"),
        ("templates/registration/login.html", "Page de connexion"),
        ("templates/core/dashboard.html", "Tableau de bord"),
        ("templates/core/etudiants_list.html", "Liste des étudiants"),
        ("templates/core/etudiant_detail.html", "Détail étudiant"),
        ("templates/core/enseignants_list.html", "Liste des enseignants"),
        ("templates/core/cours_list.html", "Liste des cours"),
        ("templates/core/notes_list.html", "Gestion des notes"),
        ("templates/core/emploi_du_temps.html", "Emploi du temps"),
        ("templates/core/statistiques.html", "Page de statistiques"),
    ]
    
    for filepath, description in template_files:
        if not check_file_exists(filepath, description):
            errors += 1
    
    # Vérification des fichiers statiques
    print("\n🎨 Fichiers statiques:")
    static_files = [
        ("static/css/custom.css", "Styles personnalisés"),
        ("static/js/main.js", "JavaScript principal"),
    ]
    
    for filepath, description in static_files:
        if not check_file_exists(filepath, description):
            errors += 1
    
    # Vérification du contenu des fichiers critiques
    print("\n🔍 Vérification du contenu:")
    
    # Vérifier settings.py
    if not check_file_content("school_management/settings.py", "INSTALLED_APPS", "Configuration INSTALLED_APPS"):
        warnings += 1
    
    if not check_file_content("school_management/settings.py", "'core'", "Application core dans INSTALLED_APPS"):
        warnings += 1
    
    # Vérifier models.py
    if not check_file_content("core/models.py", "class Etudiant", "Modèle Etudiant"):
        warnings += 1
    
    if not check_file_content("core/models.py", "class Enseignant", "Modèle Enseignant"):
        warnings += 1
    
    # Vérifier views.py
    if not check_file_content("core/views.py", "def dashboard", "Vue dashboard"):
        warnings += 1
    
    # Vérifier urls.py
    if not check_file_content("core/urls.py", "dashboard", "URL dashboard"):
        warnings += 1
    
    # Vérifier requirements.txt
    if not check_file_content("requirements.txt", "Django", "Django dans requirements"):
        warnings += 1
    
    # Résumé final
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DE LA VÉRIFICATION")
    print("=" * 50)
    
    if errors == 0 and warnings == 0:
        print("🎉 PARFAIT! Tous les fichiers sont présents et correctement configurés.")
        print("✅ Le projet EduManager est prêt à être lancé!")
        print("\n🚀 Étapes suivantes:")
        print("   1. Créer un environnement virtuel: python -m venv venv")
        print("   2. Activer l'environnement: source venv/bin/activate (Linux/Mac) ou venv\\Scripts\\activate (Windows)")
        print("   3. Lancer le script: python run_server.py")
        print("   4. Ou manuellement: pip install -r requirements.txt && python manage.py migrate && python manage.py runserver")
        
    elif errors == 0:
        print(f"⚠️  ATTENTION: {warnings} avertissement(s) détecté(s)")
        print("✅ Tous les fichiers essentiels sont présents")
        print("🔧 Vérifiez les avertissements ci-dessus")
        
    else:
        print(f"❌ ERREURS: {errors} fichier(s) manquant(s)")
        if warnings > 0:
            print(f"⚠️  AVERTISSEMENTS: {warnings} problème(s) de contenu")
        print("🔧 Corrigez les erreurs avant de continuer")
        
    print(f"\n📈 Statistiques:")
    print(f"   - Fichiers vérifiés: {len(files_to_check) + len(django_files) + len(core_files) + len(template_files) + len(static_files)}")
    print(f"   - Répertoires vérifiés: {len(directories_to_check)}")
    print(f"   - Erreurs: {errors}")
    print(f"   - Avertissements: {warnings}")
    
    # Code de sortie
    if errors > 0:
        sys.exit(1)
    elif warnings > 0:
        sys.exit(2)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
