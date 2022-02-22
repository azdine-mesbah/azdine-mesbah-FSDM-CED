from django.contrib import admin
from .models import Departement, Laboratoire, Etablissement, Enseignant, Sujet, FormationDoctorale, TypeFormationComplementaire, FormationComplementaire, LocalisationSoutenance
from .forms import LaboratoireAdminCreateForm, SujetAdminCreateForm

@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    list_display = ('intitule', 'description')
    search_fields = ('intitule',)

@admin.register(Etablissement)
class EtablissementAdmin(admin.ModelAdmin):
    list_display = ('intitule','description', 'ville','pays')
    search_fields = ('intitule','description', 'ville','pays__nom')

@admin.register(Enseignant)
class EnseignantAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'telephone', 'etablissement')
    search_fields = ('nom', 'prenom','cin','som','etablissement__intitule','etablissement__description')

@admin.register(Laboratoire)
class LaboratoireAdmin(admin.ModelAdmin):
    list_display = ('acronyme', 'intitule','departement','formation_doctorale')
    search_fields = ('intitule', 'acronyme','departement__intitule')
    list_filter = ('departement','formation_doctorale')
    autocomplete_fields = ('departement','formation_doctorale')
    form = LaboratoireAdminCreateForm

@admin.register(Sujet)
class SujetAdmin(admin.ModelAdmin):
    list_display = ('intitule', 'annee', 'laboratoire', 'co_directeur', 'created_at')
    search_fields = ('intitule', 'annee__intitule', 'laboratoire__intitule','laboratoire__acronyme')
    list_filter = ('laboratoire',)
    autocomplete_fields = ('annee', 'laboratoire', 'directeur', 'co_directeur')
    exclude = ('directeur',)
    form = SujetAdminCreateForm

    def save_model(self, request, obj, form, change):
        obj.directeur = form.cleaned_data['laboratoire'].get_current_directeur()
        if obj.co_directeur and obj.co_directeur.pk == obj.directeur.pk:
            obj.co_directeur = None
        return super().save_model(request, obj, form, change)

@admin.register(FormationDoctorale)
class FormationDoctoraleAdmin(admin.ModelAdmin):
    list_display = ('intitule',)
    search_fields = ('intitule','acronyme','co_ordonateur__nom', 'co_ordonateur__prenom','co_ordonateur__cin','co_ordonateur__som')
    autocomplete_fields = ('co_ordonateur',)

@admin.register(TypeFormationComplementaire)
class TypeFormationComplementaireAdmin(admin.ModelAdmin):
    list_display = ('intitule',)
    search_fields = ('intitule',)

@admin.register(FormationComplementaire)
class TypeFormationComplementaireAdmin(admin.ModelAdmin):
    list_display = ('intitule','type')
    search_fields = ('intitule','type__intitule')

@admin.register(LocalisationSoutenance)
class LocalisationSoutenanceAdmin(admin.ModelAdmin):
    list_display = ('intitule','etablissement')
    search_fields = ('intitule','etablissement__intitule','etablissement__ville')
    autocomplete_fields = ('etablissement',)