#!/bin/bash

# Script de démarrage pour EduManager
echo "Démarrage d'EduManager..."

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur si nécessaire (optionnel)
# python manage.py createsuperuser --noinput

# Démarrer le serveur
gunicorn school_management.wsgi:application --bind 0.0.0.0:$PORT
