from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from Administration.models import Departement, Enseignant, Laboratoire, Sujet, Etablissement
from CED_Tools.models import Pays, Annee
from Etudiant.models import Doctorant, Inscription, Publication
def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'welcome.html')


@login_required(login_url=settings.LOGIN_URL)
def dashboard(request):
    data = {
        'departements':Departement.objects.all(),
        'etablissements':Etablissement.objects.all(),
        'enseignants':Enseignant.objects.all(),
        'pays':Pays.objects.all(),
        'doctorants':Doctorant.objects.all(),
        'annees':Annee.objects.all()[:10],
        'inscriptions':Inscription.objects.all(),
        'laboratoires':Laboratoire.objects.all(),
        'sujets':Sujet.objects.all(),
        'publications':[sum([inscription.publications.count() for inscription in annee.inscriptions.all()]) for annee in Annee.objects.all()[:10]],
        'formations':0,
    }
    return render(request, 'dashboard.html', data)