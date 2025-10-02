# Dockerfile pour EduManager
FROM python:3.9-slim

# Définir les variables d'environnement
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Créer et définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . /app/

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

# Créer un utilisateur non-root
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Exposer le port
EXPOSE 8000

# Commande par défaut
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "school_management.wsgi:application"]
