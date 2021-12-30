from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from Administration.models import Departement, Enseignant, Laboratoire, Sujet
from Etudiant.models import Doctorant, Inscription
def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'welcome.html')


@login_required(login_url=settings.LOGIN_URL)
def dashboard(request):
    data = {
        'departements':Departement.objects.count(),
        'enseignants':Enseignant.objects.count(),
        'doctorants':Doctorant.objects.count(),
        'inscriptions':Inscription.objects.count(),
        'laboratoires':Laboratoire.objects.count(),
        'sujets':Sujet.objects.count(),
        'publications':0,
        'formations':0,
    }
    return render(request, 'dashboard.html', data)