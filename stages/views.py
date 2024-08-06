from .forms import DemandeForm, StagiaireForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Demande, Departement, Stagiaire, Rh, RespoDepartements
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail

def home(request):
    return redirect('homee')

def home_view(request):
    return render(request, 'stages/home.html')

def soumettre_stagiaire(request):
    if request.method == 'POST':
        form = StagiaireForm(request.POST)
        if form.is_valid():
            stagiaire = form.save()
            return redirect('soumettre_demande', stagiaire_id=stagiaire.id)
    else:
        form = StagiaireForm()
    return render(request, 'stages/soumettre_stagiaire.html', {'form': form})

def soumettre_demande(request, stagiaire_id):
    stagiaire = get_object_or_404(Stagiaire, id=stagiaire_id)
    if request.method == 'POST':
        form = DemandeForm(request.POST, request.FILES)
        if form.is_valid():
            demande = form.save(commit=False)
            demande.stagiaire = stagiaire
            if 'lettre_motivation' in request.FILES:
                demande.lettre_motivation = request.FILES['lettre_motivation']
            if 'cv' in request.FILES:
                demande.cv = request.FILES['cv']
            demande.save()
            return redirect('demande_soumise', stagiaire_id=stagiaire_id)
    else:
        form = DemandeForm()
    return render(request, 'stages/soumettre_demande.html', {'form': form, 'stagiaire': stagiaire})

def demande_soumise(request, stagiaire_id):
    return render(request, 'stages/demande_soumise.html', {'stagiaire_id': stagiaire_id})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_type = request.POST.get('user_type')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user_type == 'RH' and user.groups.filter(name='RH').exists():
                login(request, user)
                return redirect('home')
            elif user_type == 'Responsable' and user.groups.filter(name='Responsable').exists():
                login(request, user)
                return redirect('home_responsable')
            else:
                return render(request, 'stages/login.html', {'error': 'You do not have permission to view this page.'})
        else:
            return render(request, 'stages/login.html', {'error': 'Invalid username or password'})
    return render(request, 'stages/login.html')

def is_rh(user):
    return user.groups.filter(name='RH').exists()

@login_required
@user_passes_test(is_rh)
def demande_list(request):
    demandes = Demande.objects.filter(envoie_responsable=False)
    return render(request, 'stages/demande_list.html', {'demandes': demandes})

@login_required
@user_passes_test(is_rh)
def demande_detail(request, demande_id):
    demande = get_object_or_404(Demande, id=demande_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'valider':
            demande.envoie_responsable = True
            demande.save()
        
        elif action == 'refuser':
            demande.statut = 'RF'
            demande.raison_refus = request.POST.get('raison_refus')
            demande.save()
        
        return redirect('demande_list')
    
    responsables = RespoDepartements.objects.all()
    return render(request, 'stages/demande_detail.html', {'demande': demande, 'responsables': responsables})

def envoyer_notification_email(email, statut):
    sujet = f"Votre demande de stage a été {statut}"
    message = f"Bonjour,\n\nVotre demande de stage a été {statut}.\n\nCordialement,\nL'équipe RH"
    send_mail(sujet, message, 'votre_email@gmail.com', [email])

def send_email_notification(email, status):
    subject = f"Resultat de votre demande"
    message = f"Bonjour,\n\nVotre demande de stage a été {status}.\n\nCordialement,\nL'équipe RH"
    send_mail(subject, message, 'your_email@example.com', [email])

def logout_view(request):
    logout(request)
    return redirect('login')

def add_user_to_rh_group(rh_instance):
    group, created = Group.objects.get_or_create(name='RH')
    rh_instance.user.groups.add(group)

def search_demands(request):
    query = request.GET.get('search')
    if query:
        demandes = Demande.objects.filter(stagiaire__nom__icontains(query))
    else:
        demandes = Demande.objects.all()
    return render(request, 'stages/demande_list.html', {'demandes': demandes, 'query': query})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='RH').exists())
def demande_list_accepte(request):
    demandes = Demande.objects.filter(responsable_validated=True, statut='EC')
    
    if request.method == 'POST':
        demande_id = request.POST.get('demande_id')
        action = request.POST.get('action')
        demande = get_object_or_404(Demande, id=demande_id)
        
        if action == 'accepter':
            demande.statut = 'AC'
        
        demande.save()
        return redirect('demande_list_accepte')
    
    return render(request, 'stages/demande_list_accepte.html', {'demandes': demandes})

def is_responsable(user):
    return user.groups.filter(name='Responsable').exists()

@login_required
@user_passes_test(is_responsable)
def home_responsable_view(request):
    return render(request, 'stages/home_responsable.html')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Responsable').exists())
def demande_list_RH(request):
    demandes = Demande.objects.filter(envoie_responsable=True, responsable_validated=False)
    
    if request.method == 'POST':
        demande_id = request.POST.get('demande_id')
        action = request.POST.get('action')
        demande = get_object_or_404(Demande, id=demande_id)
        
        if action == 'accepter':
            demande.responsable_validated = True
        elif action == 'refuser':
            demande.statut = 'RF'
            demande.raison_refus = request.POST.get('raison_refus')
        
        demande.save()
        return redirect('demande_list_RH')
    
    return render(request, 'stages/demande_list_RH.html', {'demandes': demandes})

@login_required
@user_passes_test(is_responsable)
def demande_detail2(request, demande_id):
    demande = get_object_or_404(Demande, id=demande_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'valider':
            demande.responsable_validated = True
            demande.save()
        
        elif action == 'refuser':
            demande.statut = 'RF'
            demande.raison_refus = request.POST.get('raison_refus')
            demande.save()
        
        return redirect('demande_list_RH')
    
    return render(request, 'stages/demande_detail2.html', {'demande': demande})

@login_required
@user_passes_test(is_rh)
def demande_detail3(request, demande_id):
    demande = get_object_or_404(Demande, id=demande_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'valider':
            demande.statut = 'AC'
            demande.save()
            return redirect('demande_list_accepte')
        
        elif action == 'supprimer':
            demande.delete()
            return redirect('demande_list_accepte')
    
    return render(request, 'stages/demande_detail3.html', {'demande': demande})
