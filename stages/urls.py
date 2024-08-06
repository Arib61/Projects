from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # Vue d'accueil
    path('home/', views.home_view, name='homee'),
    path('soumettre-stagiaire/', views.soumettre_stagiaire, name='soumettre_stagiaire'),
    path('soumettre/<int:stagiaire_id>/', views.soumettre_demande, name='soumettre_demande'),
    path('demande-soumise/<int:stagiaire_id>/', views.demande_soumise, name='demande_soumise'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('demandes/', views.demande_list, name='demande_list'),
    path('demandes/<int:demande_id>/', views.demande_detail, name='demande_detail'),
    path('search/', views.search_demands, name='search_demands'),
    path('stages/demandes_acceptees/', views.demande_list_accepte, name='demande_list_accepte'),
    path('home_responsable/', views.home_responsable_view, name='home_responsable'),
    path('demandes_responsable/', views.demande_list_RH, name='demande_list_RH'),
    path('demandes_validees_rh/', views.demande_list_RH, name='demande_list_RH'),
    path('demandes/<int:demande_id>/detail2/', views.demande_detail2, name='demande_detail2'),
    path('demandes/<int:demande_id>/detail3/', views.demande_detail3, name='demande_detail3'),
]
