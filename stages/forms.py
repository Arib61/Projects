# stages/forms.py

from django import forms
from .models import Demande, Stagiaire


class StagiaireForm(forms.ModelForm):
    class Meta:
        model = Stagiaire
        fields = ['nom', 'prenom', 'email', 'telephone', 'date_naissance', 'annee_etude', 'etablissement']
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }

class DemandeForm(forms.ModelForm):
    #Class demandeFrom qui hetire du forms.ModelForm
    class Meta:
        model = Demande #Formulaire basé sur le model Demande
        fields = ['date_soumission', 'mode', 'sujet', 'duree', 'type','lettre_motivation','cv'] #Champs du model Demande qui seront unclus dans le formulaire
        #le champ date_soumission utilisera un widget DateInput
        widgets = {
            'date_soumission': forms.DateInput(attrs={'type': 'date'}),
        }

