from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Departement, Laboratoire, Enseignant, Sujet
from .forms import LaboratoireCreateForm, SujetCreateForm
from django.db.models.signals import post_save

@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    list_display = ('intitule', 'description')
    search_fields = ('intitule',)

@admin.register(Enseignant)
class EnseignantAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'telephone', 'etablissement')
    search_fields = ('nom', 'prenom','etablissement')

@admin.register(Laboratoire)
class LaboratoireAdmin(admin.ModelAdmin):
    list_display = ('acronyme', 'intitule','departement')
    search_fields = ('intitule', 'acronyme','departement__intitule')
    list_filter = ('departement',)
    autocomplete_fields = ('departement',)
    form = LaboratoireCreateForm

    def save_model(self, request, obj, form, change):
        directeur = form.cleaned_data['directeur']
        obj.save()
        obj.directeurs.filter(courant=True).update(courant=False)
        directeur.laboratoires.filter(courant=True).update(courant=False)
        obj.directeurs.create(directeur_id = directeur.id)
        return super().save_model(request, obj, form, change)

@admin.register(Sujet)
class SujetAdmin(admin.ModelAdmin):
    list_display = ('intitule', 'annee', 'laboratoire', 'directeur', 'co_directeur')
    search_fields = ('intitule', 'annee__intitule', 'laboratoire__intitule','laboratoire__acronyme')
    list_filter = ('annee', 'laboratoire', 'directeur','co_directeur')
    autocomplete_fields = ('annee', 'laboratoire', 'directeur', 'co_directeur')
    exclude = ('directeur',)
    form = SujetCreateForm

    def save_model(self, request, obj, form, change):
        obj.directeur = form.cleaned_data['laboratoire'].get_current_directeur()
        if obj.co_directeur and obj.co_directeur.pk == obj.directeur.pk:
            obj.co_directeur = None
        return super().save_model(request, obj, form, change)