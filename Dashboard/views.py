from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from Administration.models import Departement, Enseignant, Laboratoire, Sujet, Etablissement, FormationDoctorale
from CED_Tools.models import Pays, Annee
from Etudiant.models import Doctorant, Inscription, Publication
def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'welcome.html')


@login_required(login_url=settings.LOGIN_URL)
def dashboard(request):
    departements = Departement.objects.all()
    etablissements = Etablissement.objects.exclude(enseignants=None)
    enseignants = Enseignant.objects.all()
    doctorants = Doctorant.objects.all()
    pays = Pays.objects.exclude(doctorants=None)
    laboratoires = Laboratoire.objects.all()
    formations = FormationDoctorale.objects.all()
    Inscriptions = Inscription.objects.all()
    sujets = Sujet.objects.all()
    publications = Publication.objects.all()
    annees = Annee.objects.order_by('-annee')[:10][::-1]
    data = {
        'departements':{
            'count':departements.count(),
            'labels':list(departements.values_list('intitule',flat=True)),
            'colors':[dep.color for dep in departements],
            'data':[dep.laboratoires.count() for dep in departements]
        },
        'enseignants':{
            'count':enseignants.count(),
            'labels':list(etablissements.values_list('intitule',flat=True)),
            'colors':[dep.color for dep in etablissements],
            'data':[dep.enseignants.count() for dep in etablissements]
        },
        'doctorants':{
            'count':doctorants.count(),
            'labels':list(pays.values_list('nom',flat=True)),
            'colors':[p.color for p in pays],
            'data':[p.doctorants.count() for p in pays]
        },
        'laboratoires':{
            'count':laboratoires.count(),
            'labels':list(laboratoires.values_list('intitule',flat=True)),
            'colors':[laboratoire.color for laboratoire in laboratoires],
            'data':[laboratoire.sujets.count() for laboratoire in laboratoires]
        },
        'formations':{
            'count':formations.count(),
            'labels':list(formations.values_list('intitule',flat=True)),
            'colors':[formation.color for formation in formations],
            'data':[formation.formations_complementaires.count() for formation in formations]
        },
        'inscriptions':{
            'count':Inscriptions.count(),
            'labels':[annee.intitule for annee in annees],
            'colors':[annee.color for annee in annees],
            'data':[annee.inscriptions.count() for annee in annees],
        },
        
        'sujets':{
            'count':sujets.count(),
            'labels':[annee.intitule for annee in annees],
            'colors':[annee.color for annee in annees],
            'data':[annee.sujets.count() for annee in annees],
        },
        'publications':{
            'count':publications.count(),
            'labels':[annee.intitule for annee in annees],
            'colors':[annee.color for annee in annees],
            'data':[sum([inscription.publications.count() for inscription in annee.inscriptions.all()]) for annee in annees],
        }        
    }
    return render(request, 'dashboard.html', data)