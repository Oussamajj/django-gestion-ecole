from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML
from .models import (
    Etudiant, Enseignant, Cours, Note, EmploiDuTemps, 
    Message, Notification, ProfilUtilisateur, Departement, Classe
)


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Nom d\'utilisateur',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre nom d\'utilisateur'
        })
    )
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre mot de passe'
        })
    )


class EtudiantForm(forms.ModelForm):
    first_name = forms.CharField(label='Prénom', max_length=30)
    last_name = forms.CharField(label='Nom', max_length=30)
    email = forms.EmailField(label='Email')
    
    class Meta:
        model = Etudiant
        fields = ['numero_etudiant', 'classe', 'date_naissance', 'telephone', 'adresse']
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'adresse': forms.Textarea(attrs={'rows': 3}),
        }


class EnseignantForm(forms.ModelForm):
    first_name = forms.CharField(label='Prénom', max_length=30)
    last_name = forms.CharField(label='Nom', max_length=30)
    email = forms.EmailField(label='Email')
    
    class Meta:
        model = Enseignant
        fields = ['departement', 'telephone', 'adresse', 'date_embauche']
        widgets = {
            'date_embauche': forms.DateInput(attrs={'type': 'date'}),
            'adresse': forms.Textarea(attrs={'rows': 3}),
        }


class CoursForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = ['matiere', 'enseignant', 'classe', 'semestre', 'annee_scolaire']


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['etudiant', 'cours', 'type_evaluation', 'note', 'coefficient', 'date_evaluation', 'commentaire']
        widgets = {
            'date_evaluation': forms.DateInput(attrs={'type': 'date'}),
            'commentaire': forms.Textarea(attrs={'rows': 3}),
        }


class EmploiDuTempsForm(forms.ModelForm):
    class Meta:
        model = EmploiDuTemps
        fields = ['cours', 'jour', 'heure_debut', 'heure_fin', 'type_cours', 'salle']
        widgets = {
            'heure_debut': forms.TimeInput(attrs={'type': 'time'}),
            'heure_fin': forms.TimeInput(attrs={'type': 'time'}),
        }


class MessageForm(forms.ModelForm):
    destinataires = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    
    envoyer_a_tous_enseignants = forms.BooleanField(required=False)
    envoyer_a_tous_etudiants = forms.BooleanField(required=False)

    class Meta:
        model = Message
        fields = ['sujet', 'contenu', 'important']

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if user:
            if user.is_superuser:
                self.fields['destinataires'].queryset = User.objects.exclude(id=user.id)
            else:
                self.fields['destinataires'].queryset = User.objects.filter(is_superuser=True)


class ChangerMotDePasseForm(forms.Form):
    ancien_mot_de_passe = forms.CharField(
        widget=forms.PasswordInput(),
        required=False
    )
    nouveau_mot_de_passe = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=8
    )
    confirmer_mot_de_passe = forms.CharField(
        widget=forms.PasswordInput()
    )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        
        # Si c'est un mot de passe temporaire, pas besoin de l'ancien
        if user and hasattr(user, 'profil') and user.profil and user.profil.mot_de_passe_temporaire:
            self.fields['ancien_mot_de_passe'].required = False
        else:
            self.fields['ancien_mot_de_passe'].required = True

    def clean(self):
        cleaned_data = super().clean()
        nouveau = cleaned_data.get('nouveau_mot_de_passe')
        confirmer = cleaned_data.get('confirmer_mot_de_passe')
        ancien = cleaned_data.get('ancien_mot_de_passe')

        if nouveau and confirmer:
            if nouveau != confirmer:
                raise forms.ValidationError("Les mots de passe ne correspondent pas.")

        if self.user and ancien and self.fields['ancien_mot_de_passe'].required:
            if not self.user.check_password(ancien):
                raise forms.ValidationError("L'ancien mot de passe est incorrect.")

        return cleaned_data


class CreerUtilisateurForm(forms.ModelForm):
    type_utilisateur = forms.ChoiceField(
        choices=[
            ('etudiant', 'Étudiant'),
            ('enseignant', 'Enseignant'),
        ]
    )
    
    numero_etudiant = forms.CharField(max_length=20, required=False)
    classe = forms.ModelChoiceField(queryset=Classe.objects.all(), required=False)
    departement = forms.ModelChoiceField(queryset=Departement.objects.all(), required=False)
    date_embauche = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    telephone = forms.CharField(max_length=15, required=False)
    adresse = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))
    date_naissance = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    envoyer_email = forms.BooleanField(initial=True, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
