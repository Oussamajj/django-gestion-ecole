# 📚 EduManager - Guide Utilisateur Complet

## 🎯 **Vue d'Ensemble**

EduManager est un système de gestion scolaire complet qui permet de gérer les étudiants, enseignants, cours, notes, et bien plus encore. Ce guide vous explique comment utiliser toutes les fonctionnalités selon votre rôle.

---

## 🔐 **Connexion au Système**

### **Comptes de Test Disponibles :**

#### **👑 Administrateur :**
```
Identifiant : admin
Mot de passe : admin123
Accès : Toutes les fonctionnalités
```

#### **👨‍🏫 Enseignant :**
```
Identifiant : prof1
Mot de passe : prof123
Accès : Gestion des notes, messagerie, emploi du temps
```

#### **👨‍🎓 Étudiant :**
```
Identifiant : etudiant1
Mot de passe : etudiant123
Accès : Consultation des notes, messagerie, emploi du temps
```

### **Première Connexion :**
1. **Ouvrir** le navigateur et aller à l'adresse du système
2. **Entrer** vos identifiants de connexion
3. **Cliquer** sur "Se connecter"
4. **Changer** votre mot de passe si c'est temporaire

---

## 👑 **Guide Administrateur**

### **🏠 Tableau de Bord Admin**

Le tableau de bord affiche des **statistiques en temps réel** :
- **Connexions** aujourd'hui et cette semaine
- **Activité récente** (notes, messages)
- **Utilisateurs actifs**
- **Mots de passe temporaires** à changer

### **👥 Gestion des Utilisateurs**

#### **Accéder à la Gestion :**
1. **Cliquer** sur "Gestion Utilisateurs" dans la sidebar
2. **Voir** la liste complète des utilisateurs avec leurs informations

#### **Fonctionnalités Disponibles :**

##### **👁️ Voir les Mots de Passe :**
1. **Cliquer** sur l'icône 👁️ (œil) dans la colonne "Mot de passe"
2. **Le vrai mot de passe** s'affiche (dernier défini ou par défaut)
3. **Cliquer** à nouveau pour masquer

##### **✏️ Modifier les Mots de Passe :**
1. **Cliquer** sur l'icône ✏️ (crayon) dans la colonne "Mot de passe"
2. **Entrer** le nouveau mot de passe (minimum 8 caractères)
3. **Confirmer** - Le système stocke et affiche le nouveau mot de passe

##### **🔑 Réinitialiser les Mots de Passe :**
1. **Cliquer** sur l'icône 🔑 (clé) dans la colonne "Actions"
2. **Confirmer** la réinitialisation
3. **Un mot de passe** est généré automatiquement
4. **L'utilisateur** reçoit une notification

##### **👤 Modifier un Utilisateur :**
1. **Cliquer** sur l'icône ✏️ (crayon) dans la colonne "Actions"
2. **Modifier** les informations (nom, prénom, email, téléphone)
3. **Activer/Désactiver** le compte
4. **Enregistrer** les modifications

##### **🔄 Activer/Désactiver un Compte :**
1. **Cliquer** sur l'icône 🚫 (interdiction) dans la colonne "Actions"
2. **Confirmer** le changement de statut
3. **L'utilisateur** reçoit une notification automatique

### **👨‍🎓 Gestion des Étudiants**

#### **Ajouter un Étudiant :**
1. **Aller** à "Étudiants" → **Cliquer** "Ajouter un Étudiant"
2. **Remplir** les informations :
   - Prénom, Nom, Email (obligatoires)
   - Numéro étudiant (généré automatiquement si vide)
   - Classe, Date de naissance, Téléphone, Adresse
3. **Enregistrer** - Un compte utilisateur est créé automatiquement

#### **Modifier un Étudiant :**
1. **Dans la liste** des étudiants, **cliquer** l'icône ✏️
2. **Modifier** les informations nécessaires
3. **Enregistrer** les modifications

#### **Supprimer un Étudiant :**
1. **Cliquer** l'icône 🗑️ dans la liste
2. **Lire** les avertissements (suppression du compte, notes, etc.)
3. **Confirmer** la suppression définitive

### **👨‍🏫 Gestion des Enseignants**

#### **Ajouter un Enseignant :**
1. **Aller** à "Enseignants" → **Cliquer** "Nouvel Enseignant"
2. **Remplir** les informations :
   - Prénom, Nom, Email (obligatoires)
   - Département, Date d'embauche, Téléphone, Adresse
3. **Enregistrer** - Un compte utilisateur est créé automatiquement

#### **Modifier/Supprimer :**
- **Même processus** que pour les étudiants
- **Attention** : Supprimer un enseignant supprime aussi ses cours et notes

### **📚 Gestion des Cours**

#### **Ajouter un Cours :**
1. **Aller** à "Cours" → **Cliquer** "Nouveau Cours"
2. **Sélectionner** :
   - Matière et Enseignant (obligatoires)
   - Classe et Semestre
   - Année scolaire et Coefficient
3. **Ajouter** une description si nécessaire

#### **Modifier/Supprimer :**
- **Utiliser** les icônes ✏️ et 🗑️ dans la liste des cours
- **Attention** : Supprimer un cours supprime toutes les notes associées

### **📊 Gestion des Notes**

#### **Ajouter une Note :**
1. **Aller** à "Notes" → **Cliquer** "Nouvelle Note"
2. **Sélectionner** :
   - Étudiant et Cours (obligatoires)
   - Note sur 20, Coefficient, Type d'évaluation
   - Date d'évaluation et Semestre
3. **Ajouter** un commentaire si nécessaire

#### **Modifier/Supprimer :**
- **Utiliser** les icônes dans la liste des notes
- **La moyenne** de l'étudiant est recalculée automatiquement

---

## 👨‍🏫 **Guide Enseignant**

### **🏠 Tableau de Bord Enseignant**

Affiche :
- **Vos cours** assignés
- **Nombre d'étudiants** que vous enseignez
- **Emploi du temps** de la semaine
- **Messages** et notifications récents

### **📊 Gestion des Notes**

#### **Ajouter des Notes :**
1. **Aller** à "Notes" → **Cliquer** "Nouvelle Note"
2. **Sélectionner** un de vos cours
3. **Choisir** l'étudiant et entrer la note
4. **Enregistrer**

#### **Modifier des Notes :**
- **Vous pouvez** modifier les notes de vos cours uniquement
- **Utiliser** l'icône ✏️ dans la liste

### **📚 Consultation des Cours**

1. **Aller** à "Cours" pour voir vos cours assignés
2. **Voir** les détails : classe, horaires, étudiants inscrits
3. **Consulter** l'emploi du temps

### **💬 Messagerie**

#### **Envoyer un Message :**
1. **Aller** à "Messagerie" → **Onglet** "Envoyer"
2. **Sélectionner** les destinataires :
   - Étudiants de vos classes
   - Autres enseignants
   - Administration
3. **Écrire** le message et **envoyer**

#### **Consulter les Messages :**
1. **Onglet** "Reçus" pour les messages reçus
2. **Onglet** "Envoyés" pour vos messages envoyés
3. **Marquer** comme lu/non lu

---

## 👨‍🎓 **Guide Étudiant**

### **🏠 Tableau de Bord Étudiant**

Affiche :
- **Votre moyenne générale**
- **Vos dernières notes**
- **Vos cours** de la classe
- **Emploi du temps** de la semaine

### **📊 Consultation des Notes**

1. **Aller** à "Notes" pour voir toutes vos notes
2. **Filtrer** par matière ou période
3. **Voir** les détails : note, coefficient, type d'évaluation, commentaires
4. **Consulter** votre moyenne par matière

### **📚 Consultation des Cours**

1. **Voir** les cours de votre classe
2. **Consulter** les informations : enseignant, horaires, salle
3. **Vérifier** l'emploi du temps

### **💬 Messagerie**

#### **Envoyer un Message :**
1. **Aller** à "Messagerie" → **Onglet** "Envoyer"
2. **Sélectionner** les destinataires :
   - Vos enseignants
   - L'administration
   - Autres étudiants (si autorisé)
3. **Écrire** et **envoyer** le message

#### **Consulter les Messages :**
- **Même interface** que pour les enseignants
- **Recevoir** les messages de l'administration et des enseignants

---

## 🔧 **Fonctionnalités Communes**

### **🔐 Changer son Mot de Passe**

1. **Cliquer** sur "Changer mot de passe" dans la sidebar
2. **Entrer** l'ancien mot de passe (si pas temporaire)
3. **Entrer** le nouveau mot de passe (minimum 8 caractères)
4. **Confirmer** le nouveau mot de passe
5. **Enregistrer**

### **🔔 Notifications**

1. **Cliquer** sur "Notifications" dans la sidebar
2. **Voir** toutes vos notifications :
   - Changements de mot de passe
   - Messages importants
   - Alertes système
3. **Marquer** comme lu/non lu

### **🚪 Déconnexion**

1. **Cliquer** sur le bouton rouge "Déconnexion" en bas de la sidebar
2. **Vous êtes** redirigé vers la page de connexion

---

## 🎨 **Interface et Navigation**

### **📱 Interface Responsive**

- **Compatible** avec tous les appareils (PC, tablette, mobile)
- **Menu sidebar** collapsible sur mobile
- **Design moderne** avec Bootstrap 5

### **🎨 Éléments Visuels**

#### **Codes Couleur :**
- **Bleu** : Actions de consultation (👁️)
- **Gris** : Actions de modification (✏️)
- **Rouge** : Actions de suppression (🗑️)
- **Vert** : Actions de validation (✅)
- **Orange** : Actions d'attention (⚠️)

#### **Icônes :**
- **👁️** : Voir/Consulter
- **✏️** : Modifier/Éditer
- **🗑️** : Supprimer
- **🔑** : Réinitialiser mot de passe
- **🚫** : Activer/Désactiver
- **➕** : Ajouter/Créer

### **📊 Tableaux et Listes**

- **Pagination** automatique pour les grandes listes
- **Recherche** et **filtres** disponibles
- **Tri** par colonnes (cliquer sur les en-têtes)
- **Actions groupées** pour les administrateurs

---

## 🔍 **Recherche et Filtres**

### **🔍 Recherche Globale**

Dans chaque section :
1. **Utiliser** la barre de recherche en haut
2. **Taper** le nom, prénom, email, ou identifiant
3. **Appuyer** Entrée ou cliquer "Rechercher"

### **🎛️ Filtres Avancés**

#### **Étudiants :**
- Filtrer par **classe**
- Filtrer par **niveau**

#### **Enseignants :**
- Filtrer par **département**

#### **Notes :**
- Filtrer par **étudiant**
- Filtrer par **matière**
- Filtrer par **type d'évaluation**

#### **Messages :**
- Filtrer par **type** (reçu/envoyé)
- Filtrer par **statut** (lu/non lu)

---

## 📊 **Statistiques et Rapports**

### **📈 Tableau de Bord Admin**

- **Connexions** en temps réel
- **Activité** des utilisateurs
- **Statistiques** des notes
- **Messages** et notifications

### **📊 Moyennes et Notes**

- **Calcul automatique** des moyennes
- **Pondération** par coefficient
- **Historique** des évaluations
- **Graphiques** de progression (si disponible)

---

## 🛠️ **Dépannage**

### **❓ Problèmes Courants**

#### **🔐 Problème de Connexion :**
- **Vérifier** l'identifiant et le mot de passe
- **Contacter** l'administrateur si mot de passe oublié
- **Vérifier** que le compte est actif

#### **🚫 Accès Refusé :**
- **Vérifier** vos permissions
- **Seuls les admins** peuvent ajouter des utilisateurs
- **Contacter** l'administrateur pour les droits

#### **💾 Données Non Sauvegardées :**
- **Vérifier** que tous les champs obligatoires sont remplis
- **Regarder** les messages d'erreur en rouge
- **Réessayer** l'opération

### **📞 Support**

En cas de problème :
1. **Noter** le message d'erreur exact
2. **Noter** les étapes qui ont causé le problème
3. **Contacter** l'administrateur système
4. **Fournir** votre identifiant et l'heure du problème

---

## 🎯 **Bonnes Pratiques**

### **🔐 Sécurité**

- **Changer** votre mot de passe temporaire immédiatement
- **Utiliser** un mot de passe fort (8+ caractères)
- **Se déconnecter** après utilisation
- **Ne pas partager** vos identifiants

### **📝 Saisie des Données**

- **Vérifier** l'orthographe des noms et prénoms
- **Utiliser** des emails valides
- **Remplir** tous les champs obligatoires (*)
- **Sauvegarder** régulièrement

### **💬 Communication**

- **Utiliser** la messagerie interne pour la communication officielle
- **Être** respectueux dans les messages
- **Marquer** les messages importants
- **Répondre** aux messages dans un délai raisonnable

---

## 🚀 **Conclusion**

EduManager est un système complet qui facilite la gestion scolaire. Chaque rôle a accès aux fonctionnalités appropriées avec une interface intuitive et moderne.

**Pour toute question ou suggestion d'amélioration, contactez l'équipe de développement.**

**🎓 Bonne utilisation d'EduManager ! ✨**
