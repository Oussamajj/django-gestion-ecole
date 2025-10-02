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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'Se connecter', css_class='btn btn-primary w-100')
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('departement', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('telephone', css_class='form-group col-md-6 mb-0'),
                Column('date_embauche', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'adresse',
            'avatar',
            Submit('submit', 'Enregistrer', css_class='btn btn-success')
        )


class CoursForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = ['matiere', 'enseignant', 'classe', 'semestre', 'annee_scolaire']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('matiere', css_class='form-group col-md-6 mb-0'),
                Column('enseignant', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('classe', css_class='form-group col-md-4 mb-0'),
                Column('semestre', css_class='form-group col-md-4 mb-0'),
                Column('annee_scolaire', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Enregistrer', css_class='btn btn-success')
        )


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['etudiant', 'cours', 'type_evaluation', 'note', 'coefficient', 'date_evaluation', 'commentaire']
        widgets = {
            'date_evaluation': forms.DateInput(attrs={'type': 'date'}),
            'commentaire': forms.Textarea(attrs={'rows': 3}),
            'note': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '20'}),
            'coefficient': forms.NumberInput(attrs={'step': '0.1', 'min': '0.1', 'max': '10'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('etudiant', css_class='form-group col-md-6 mb-0'),
                Column('cours', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('type_evaluation', css_class='form-group col-md-4 mb-0'),
                Column('note', css_class='form-group col-md-4 mb-0'),
                Column('coefficient', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            'date_evaluation',
            'commentaire',
            Submit('submit', 'Enregistrer', css_class='btn btn-success')
        )


class EmploiDuTempsForm(forms.ModelForm):
    class Meta:
        model = EmploiDuTemps
        fields = ['cours', 'jour', 'heure_debut', 'heure_fin', 'type_cours', 'salle']
        widgets = {
            'heure_debut': forms.TimeInput(attrs={'type': 'time'}),
            'heure_fin': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'cours',
            Row(
                Column('jour', css_class='form-group col-md-4 mb-0'),
                Column('heure_debut', css_class='form-group col-md-4 mb-0'),
                Column('heure_fin', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('type_cours', css_class='form-group col-md-6 mb-0'),
                Column('salle', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Enregistrer', css_class='btn btn-success')
        )


# Nouveaux formulaires pour la gestion avancée

class CreerUtilisateurForm(forms.ModelForm):
    """Formulaire pour créer un nouvel utilisateur (admin uniquement)"""
    type_utilisateur = forms.ChoiceField(
        choices=[
            ('etudiant', 'Étudiant'),
            ('enseignant', 'Enseignant'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # Champs spécifiques étudiant
    numero_etudiant = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    classe = forms.ModelChoiceField(
        queryset=Classe.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # Champs spécifiques enseignant
    departement = forms.ModelChoiceField(
        queryset=Departement.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_embauche = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    # Champs communs
    telephone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    adresse = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    date_naissance = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    envoyer_email = forms.BooleanField(
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class MessageForm(forms.ModelForm):
    """Formulaire pour envoyer un message"""
    destinataires = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )
    
    envoyer_a_tous_enseignants = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    envoyer_a_tous_etudiants = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Message
        fields = ['sujet', 'contenu', 'important']
        widgets = {
            'sujet': forms.TextInput(attrs={'class': 'form-control'}),
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if user:
            # Filtrer les destinataires selon le type d'utilisateur
            if user.is_superuser:
                # Admin peut envoyer à tout le monde
                self.fields['destinataires'].queryset = User.objects.exclude(id=user.id)
            else:
                # Pour les autres utilisateurs, permettre d'envoyer aux admins
                self.fields['destinataires'].queryset = User.objects.filter(is_superuser=True)


class ChangerMotDePasseForm(forms.Form):
    """Formulaire pour changer le mot de passe"""
    ancien_mot_de_passe = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    nouveau_mot_de_passe = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8
    )
    confirmer_mot_de_passe = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        nouveau = cleaned_data.get('nouveau_mot_de_passe')
        confirmer = cleaned_data.get('confirmer_mot_de_passe')

        if nouveau and confirmer:
            if nouveau != confirmer:
                raise forms.ValidationError("Les mots de passe ne correspondent pas.")

        return cleaned_data
