from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Stagiaire(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=15)
    date_naissance = models.DateField()
    annee_etude = models.CharField(max_length=50)
    etablissement = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Rh(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()

class Direction(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()

class Departement(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)

class Chef(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    departement = models.ForeignKey(Departement,on_delete = models.CASCADE)


class Demande(models.Model):
    date_soumission = models.DateField()
    STATUT_CHOICES = [
        ('EC', 'En cours'),
        ('RF', 'Refusé'),
        ('AC', 'Accepté'),
    ]
    TYPE_CHOICES = [
        ('OBS', 'Observation'),
        ('APP', 'Application'),
        ('PFE', 'PFE'),
    ]
    MODE_CHOICES = [
        ('hybride', 'Hybride'),
        ('presentiel', 'Présentiel'),
        ('adistance', 'À distance'),
    ]
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='EC')
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='Présentiel')
    sujet = models.CharField(max_length=100)
    duree = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='OBS')
    stagiaire = models.ForeignKey(Stagiaire, on_delete=models.CASCADE)
    lettre_motivation = models.FileField(upload_to='lettres_motivation/', null=True, blank=True)
    cv = models.FileField(upload_to='cvs/', null=True, blank=True)
    envoie_responsable = models.BooleanField(default=False)
    responsable_validated = models.BooleanField(default=False)
    raison_refus = models.TextField(null=True, blank=True)


class Rapport(models.Model):
    date_soumission = models.DateField()
    contenu = models.FileField(upload_to='rapports/')
    note = models.CharField(max_length=50)
    stagiaire = models.ForeignKey(Stagiaire, on_delete=models.CASCADE)
    chef = models.ForeignKey(Chef,on_delete=models.CASCADE)

class Attestation(models.Model):
    date_delivrance = models.DateField()
    contenu = models.FileField(upload_to='attestation/')
    stagiaire = models.ForeignKey(Stagiaire, on_delete=models.CASCADE)
    chef = models.ForeignKey(Chef,on_delete=models.CASCADE)

class Stagiaire_Direction(models.Model):
    stagiaire = models.ForeignKey(Stagiaire,on_delete=models.CASCADE)
    direction = models.ForeignKey(Direction,on_delete=models.CASCADE)

class Stagiaire_Departement(models.Model):
    stagiaire = models.ForeignKey(Stagiaire,on_delete=models.CASCADE)
    departement = models.ForeignKey(Departement,on_delete=models.CASCADE)



class RespoDepartements(models.Model):
    nom = models.CharField(max_length=100)
    departement = models.ForeignKey(Departement,on_delete=models.CASCADE)

