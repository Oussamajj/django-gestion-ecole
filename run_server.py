#!/usr/bin/env python
"""
Script de lancement rapide pour EduManager
Ce script automatise les étapes de configuration et de lancement du serveur
"""

import os
import sys
import subprocess
import platform

def run_command(command, description=""):
    """Exécuter une commande et afficher le résultat"""
    if description:
        print(f"\n🔄 {description}...")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(f"✅ {description} - Succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de {description}")
        print(f"Erreur: {e.stderr}")
        return False

def check_python_version():
    """Vérifier la version de Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 ou supérieur est requis")
        print(f"Version actuelle: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} détecté")
    return True

def check_virtual_env():
    """Vérifier si un environnement virtuel est activé"""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Environnement virtuel détecté")
        return True
    else:
        print("⚠️  Aucun environnement virtuel détecté")
        print("Il est recommandé d'utiliser un environnement virtuel")
        return False

def install_dependencies():
    """Installer les dépendances"""
    if not os.path.exists('requirements.txt'):
        print("❌ Fichier requirements.txt non trouvé")
        return False
    
    return run_command("pip install -r requirements.txt", "Installation des dépendances")

def setup_database():
    """Configurer la base de données"""
    print("\n📊 Configuration de la base de données...")
    
    # Créer les migrations
    if not run_command("python manage.py makemigrations", "Création des migrations"):
        return False
    
    # Appliquer les migrations
    if not run_command("python manage.py migrate", "Application des migrations"):
        return False
    
    return True

def create_superuser():
    """Créer un superutilisateur si nécessaire"""
    print("\n👤 Vérification du superutilisateur...")
    
    # Vérifier si un superutilisateur existe déjà
    check_command = 'python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).exists())"'
    
    try:
        result = subprocess.run(check_command, shell=True, capture_output=True, text=True)
        if "True" in result.stdout:
            print("✅ Superutilisateur existant trouvé")
            return True
    except:
        pass
    
    print("ℹ️  Aucun superutilisateur trouvé. Création d'un compte admin par défaut...")
    
    # Créer un superutilisateur par défaut
    create_command = """
python manage.py shell -c "
from django.contrib.auth.models import User;
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@edumanager.com', 'admin123');
    print('Superutilisateur créé: admin / admin123')
else:
    print('Utilisateur admin existe déjà')
"
"""
    
    return run_command(create_command, "Création du superutilisateur")

def create_sample_data():
    """Créer des données d'exemple"""
    print("\n📝 Voulez-vous créer des données d'exemple ? (y/N): ", end="")
    choice = input().lower()
    
    if choice in ['y', 'yes', 'o', 'oui']:
        return run_command("python manage.py create_sample_data", "Création des données d'exemple")
    
    return True

def collect_static():
    """Collecter les fichiers statiques"""
    return run_command("python manage.py collectstatic --noinput", "Collecte des fichiers statiques")

def start_server():
    """Démarrer le serveur de développement"""
    print("\n🚀 Démarrage du serveur de développement...")
    print("📍 Le serveur sera accessible à: http://127.0.0.1:8000/")
    print("🛑 Appuyez sur Ctrl+C pour arrêter le serveur")
    print("\n" + "="*50)
    
    try:
        subprocess.run("python manage.py runserver", shell=True, check=True)
    except KeyboardInterrupt:
        print("\n\n🛑 Serveur arrêté par l'utilisateur")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erreur lors du démarrage du serveur: {e}")

def main():
    """Fonction principale"""
    print("🎓 EduManager - Script de lancement automatique")
    print("=" * 50)
    
    # Vérifications préliminaires
    if not check_python_version():
        sys.exit(1)
    
    check_virtual_env()
    
    # Vérifier que nous sommes dans le bon répertoire
    if not os.path.exists('manage.py'):
        print("❌ Fichier manage.py non trouvé")
        print("Assurez-vous d'être dans le répertoire racine du projet")
        sys.exit(1)
    
    # Installation et configuration
    steps = [
        ("Installation des dépendances", install_dependencies),
        ("Configuration de la base de données", setup_database),
        ("Création du superutilisateur", create_superuser),
        ("Collecte des fichiers statiques", collect_static),
        ("Création des données d'exemple", create_sample_data),
    ]
    
    for description, func in steps:
        if not func():
            print(f"\n❌ Échec lors de: {description}")
            print("Veuillez corriger les erreurs et relancer le script")
            sys.exit(1)
    
    print("\n✅ Configuration terminée avec succès!")
    print("\n📋 Informations de connexion:")
    print("   - URL: http://127.0.0.1:8000/")
    print("   - Admin: admin / admin123")
    print("   - Interface admin: http://127.0.0.1:8000/admin/")
    
    # Démarrer le serveur
    print("\n🚀 Prêt à démarrer le serveur!")
    print("Appuyez sur Entrée pour continuer ou Ctrl+C pour quitter: ", end="")
    
    try:
        input()
        start_server()
    except KeyboardInterrupt:
        print("\n👋 Au revoir!")

if __name__ == "__main__":
    main()
