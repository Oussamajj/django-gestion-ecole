#!/usr/bin/env python
"""
Script de test pour vérifier le changement de mot de passe
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumanager.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from core.models import ProfilUtilisateur

def test_password_change():
    print("=== Test de changement de mot de passe ===")
    
    # Trouver un utilisateur étudiant
    try:
        user = User.objects.filter(etudiant__isnull=False).first()
        if not user:
            print("Aucun étudiant trouvé")
            return
            
        print(f"Utilisateur testé: {user.username} ({user.get_full_name()})")
        
        # Tester différents mots de passe possibles
        possible_passwords = ['etudiant123', 'admin123', 'prof123', 'user123', '123456', 'password']
        
        current_password = None
        for pwd in possible_passwords:
            if authenticate(username=user.username, password=pwd):
                current_password = pwd
                print(f"✅ Mot de passe actuel trouvé: {pwd}")
                break
        
        if not current_password:
            print("❌ Aucun mot de passe par défaut ne fonctionne")
            # Définir un mot de passe connu
            user.set_password('etudiant123')
            user.save()
            current_password = 'etudiant123'
            print("✅ Mot de passe réinitialisé à 'etudiant123'")
        
        # Test de changement
        new_password = 'nouveautest123'
        print(f"Changement vers: {new_password}")
        
        user.set_password(new_password)
        user.save()
        
        # Vérifier le changement
        if authenticate(username=user.username, password=new_password):
            print("✅ Changement de mot de passe réussi")
        else:
            print("❌ Échec du changement de mot de passe")
            
        # Remettre l'ancien mot de passe
        user.set_password(current_password)
        user.save()
        print(f"✅ Mot de passe restauré à: {current_password}")
        
        # Vérifier le profil
        if hasattr(user, 'profil') and user.profil:
            print(f"Profil existant - MDP temporaire: {user.profil.mot_de_passe_temporaire}")
        else:
            print("Aucun profil trouvé")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_password_change()
