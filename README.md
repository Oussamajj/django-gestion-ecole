# 🎓 EduManager - Système de Gestion Scolaire

![EduManager Logo](https://img.shields.io/badge/EduManager-v1.0-blue?style=for-the-badge&logo=graduation-cap)
![Django](https://img.shields.io/badge/Django-4.2-green?style=for-the-badge&logo=django)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?style=for-the-badge&logo=bootstrap)
![Python](https://img.shields.io/badge/Python-3.8+-yellow?style=for-the-badge&logo=python)

## 📋 Description

**EduManager** est un système de gestion scolaire moderne et responsive développé avec Django. Il offre une interface intuitive pour gérer les étudiants, enseignants, cours, notes et emplois du temps dans un établissement d'enseignement.

### ✨ Fonctionnalités Principales

- 👥 **Gestion des Étudiants** : Inscription, profils, suivi académique
- 👨‍🏫 **Gestion des Enseignants** : Profils, départements, cours assignés
- 📚 **Gestion des Cours** : Matières, crédits, planification
- 📊 **Gestion des Notes** : Évaluations, moyennes, statistiques
- 📅 **Emploi du Temps** : Planning interactif et responsive
- 📈 **Tableaux de Bord** : Statistiques et analyses en temps réel
- 🔐 **Authentification** : Système de connexion sécurisé
- 📱 **Interface Responsive** : Compatible mobile, tablette et desktop

## 🚀 Installation et Configuration

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git (optionnel)

### 1. Cloner le Projet

```bash
# Si vous utilisez Git
git clone <url-du-repository>
cd edumanager

# Ou télécharger et extraire l'archive
```

### 2. Créer un Environnement Virtuel

```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows
venv\Scripts\activate

# Sur macOS/Linux
source venv/bin/activate
```

### 3. Installer les Dépendances

```bash
pip install -r requirements.txt
```

### 4. Configuration de la Base de Données

```bash
# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser
```

### 5. Collecter les Fichiers Statiques

```bash
python manage.py collectstatic --noinput
```

### 6. Lancer le Serveur de Développement

```bash
python manage.py runserver
```

Le site sera accessible à l'adresse : `http://127.0.0.1:8000/`

## 🏗️ Structure du Projet

```
edumanager/
├── school_management/          # Configuration principale Django
│   ├── __init__.py
│   ├── settings.py            # Paramètres du projet
│   ├── urls.py               # URLs principales
│   ├── wsgi.py               # Configuration WSGI
│   └── asgi.py               # Configuration ASGI
├── core/                      # Application principale
│   ├── models.py             # Modèles de données
│   ├── views.py              # Vues et logique métier
│   ├── urls.py               # URLs de l'application
│   ├── forms.py              # Formulaires Django
│   ├── admin.py              # Interface d'administration
│   └── migrations/           # Migrations de base de données
├── templates/                 # Templates HTML
│   ├── base.html             # Template de base
│   ├── registration/         # Templates d'authentification
│   └── core/                 # Templates de l'application
├── static/                    # Fichiers statiques
│   ├── css/                  # Feuilles de style
│   ├── js/                   # Scripts JavaScript
│   └── images/               # Images et avatars
├── media/                     # Fichiers uploadés
├── requirements.txt           # Dépendances Python
└── manage.py                 # Script de gestion Django
```

## 🎨 Interface et Design

### Design System

- **Framework CSS** : Bootstrap 5.3
- **Icônes** : Font Awesome 6.4 + Bootstrap Icons
- **Couleurs** :
  - Primaire : `#2c3e50` (Bleu foncé)
  - Secondaire : `#3498db` (Bleu clair)
  - Succès : `#27ae60` (Vert)
  - Attention : `#f39c12` (Orange)
  - Danger : `#e74c3c` (Rouge)

### Fonctionnalités UI/UX

- 📱 Design responsive (mobile-first)
- 🎨 Thème moderne avec dégradés
- ⚡ Animations fluides et transitions
- 🔍 Recherche en temps réel
- 📊 Graphiques interactifs (Chart.js)
- 🎯 Navigation intuitive avec sidebar

## 📊 Modèles de Données

### Entités Principales

1. **Département** : Organise les enseignants par spécialité
2. **Classe** : Regroupe les étudiants par niveau
3. **Étudiant** : Profil étudiant avec informations personnelles
4. **Enseignant** : Profil enseignant avec département
5. **Matière** : Définit les cours avec crédits
6. **Cours** : Lie matière, enseignant et classe
7. **Note** : Évaluations avec types et coefficients
8. **EmploiDuTemps** : Planning des cours

### Relations

- Un **Enseignant** appartient à un **Département**
- Un **Étudiant** appartient à une **Classe**
- Un **Cours** lie une **Matière**, un **Enseignant** et une **Classe**
- Une **Note** concerne un **Étudiant** et un **Cours**
- Un **EmploiDuTemps** organise les **Cours** dans le temps

## 🔧 Configuration Avancée

### Variables d'Environnement

Créez un fichier `.env` à la racine du projet :

```env
SECRET_KEY=votre-clé-secrète-très-longue-et-complexe
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Configuration de Production

Pour déployer en production, modifiez `settings.py` :

```python
DEBUG = False
ALLOWED_HOSTS = ['votre-domaine.com']

# Configuration de base de données PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'edumanager_db',
        'USER': 'votre_utilisateur',
        'PASSWORD': 'votre_mot_de_passe',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 👥 Comptes de Démonstration

Après avoir créé le superutilisateur, vous pouvez créer des comptes de test :

### Administrateur
- **Utilisateur** : admin
- **Mot de passe** : admin123

### Enseignant
- **Utilisateur** : prof1
- **Mot de passe** : prof123

### Étudiant
- **Utilisateur** : etudiant1
- **Mot de passe** : etudiant123

## 📚 Utilisation

### 1. Connexion

Accédez à `http://127.0.0.1:8000/` et connectez-vous avec vos identifiants.

### 2. Navigation

- **Tableau de bord** : Vue d'ensemble avec statistiques
- **Étudiants** : Gestion des profils étudiants
- **Enseignants** : Gestion des profils enseignants
- **Cours** : Organisation des matières et cours
- **Notes** : Saisie et consultation des évaluations
- **Emploi du temps** : Planning interactif
- **Statistiques** : Analyses et rapports

### 3. Fonctionnalités par Rôle

#### Administrateur
- Accès complet à toutes les fonctionnalités
- Gestion des utilisateurs
- Configuration du système

#### Enseignant
- Consultation de ses cours
- Saisie des notes de ses étudiants
- Consultation de l'emploi du temps

#### Étudiant
- Consultation de ses notes
- Visualisation de son emploi du temps
- Accès à son profil

## 🛠️ Développement

### Ajouter de Nouvelles Fonctionnalités

1. **Créer un nouveau modèle** dans `core/models.py`
2. **Générer les migrations** : `python manage.py makemigrations`
3. **Appliquer les migrations** : `python manage.py migrate`
4. **Créer les vues** dans `core/views.py`
5. **Ajouter les URLs** dans `core/urls.py`
6. **Créer les templates** dans `templates/core/`

### Tests

```bash
# Lancer les tests
python manage.py test

# Tests avec couverture
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Commandes Utiles

```bash
# Créer une nouvelle application
python manage.py startapp nouvelle_app

# Shell Django
python manage.py shell

# Vider la base de données
python manage.py flush

# Sauvegarder les données
python manage.py dumpdata > backup.json

# Restaurer les données
python manage.py loaddata backup.json
```

## 🚀 Déploiement

### Avec Gunicorn

```bash
pip install gunicorn
gunicorn school_management.wsgi:application
```

### Avec Docker

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### Variables d'Environnement de Production

```env
SECRET_KEY=votre-clé-de-production-très-sécurisée
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com
DATABASE_URL=postgresql://user:password@localhost/edumanager_prod
```

## 🤝 Contribution

1. Fork le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Committez vos changements (`git commit -am 'Ajouter nouvelle fonctionnalité'`)
4. Poussez vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créez une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

### FAQ

**Q : Comment réinitialiser le mot de passe d'un utilisateur ?**
R : Utilisez la commande `python manage.py changepassword nom_utilisateur`

**Q : Comment sauvegarder la base de données ?**
R : Utilisez `python manage.py dumpdata > backup.json`

**Q : L'interface ne s'affiche pas correctement**
R : Vérifiez que `python manage.py collectstatic` a été exécuté

### Contact

- 📧 Email : support@edumanager.com
- 🐛 Issues : [GitHub Issues](https://github.com/votre-repo/issues)
- 📖 Documentation : [Wiki du projet](https://github.com/votre-repo/wiki)

## 🎯 Roadmap

### Version 1.1 (Prochaine)
- [ ] API REST avec Django REST Framework
- [ ] Notifications en temps réel
- [ ] Import/Export Excel
- [ ] Système de messagerie interne

### Version 1.2
- [ ] Application mobile (React Native)
- [ ] Intégration avec Google Calendar
- [ ] Système de paiement des frais
- [ ] Rapports PDF avancés

### Version 2.0
- [ ] Intelligence artificielle pour l'analyse prédictive
- [ ] Système de visioconférence intégré
- [ ] Gestion des ressources (salles, matériel)
- [ ] Multi-établissements

## 🙏 Remerciements

- [Django](https://djangoproject.com/) - Framework web Python
- [Bootstrap](https://getbootstrap.com/) - Framework CSS
- [Font Awesome](https://fontawesome.com/) - Icônes
- [Chart.js](https://chartjs.org/) - Graphiques interactifs
- La communauté open source pour les nombreuses contributions

---

**EduManager** - Simplifiez la gestion de votre établissement scolaire ! 🎓

*Développé avec ❤️ par l'équipe EduManager*
