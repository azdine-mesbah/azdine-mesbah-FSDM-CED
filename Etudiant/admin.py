from django.contrib import admin
from .models import Doctorant, CursusType, Cursus, Inscription, RetraitType, Retrait, Publication, Formation_C_Inscription, Soutenance, SoutenanceMembers
# Register your models here.

@admin.register(Doctorant)
class DoctorantAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom','cin','cne')
    list_filter = ('fonctionnaire', 'sexe')
    search_fields = ('nom','prenom','cne','cin')
    autocomplete_fields = ('pays','annee_bac')
    readonly_fields = ('photo_preview',)

    def photo_preview(self, obj):
        return obj.photo_preview

    photo_preview.short_description = 'Photo Preview'
    photo_preview.allow_tags = True

@admin.register(CursusType)
class CursusTypeAdmin(admin.ModelAdmin):
    list_display = ('intitule', 'duree_annees')
    list_filter = ('duree_annees',)
    search_fields = ('intitule',)

@admin.register(Cursus)
class CursusAdmin(admin.ModelAdmin):
    list_display = ('doctorant', 'type','specialite','annee','duree','mention')
    list_filter = ('type', 'duree')
    search_fields = ('specialite','ville','etablissement','annee__intitule','type__intitule','doctorant__nom','doctorant__prenom','doctorant__cne','doctorant__cin')
    autocomplete_fields = ('doctorant','type','annee')

@admin.register(RetraitType)
class RetraitTypeAdmin(admin.ModelAdmin):
    search_fields = ('intitule',)
    list_display = ('intitule','max_delais')

@admin.register(Retrait)
class RetraitAdmin(admin.ModelAdmin):
    list_display = ('type', 'doctorant','created_at', 'date_retour')
    list_filter = ('type',)
    search_fields = ('doctorant',)
    autocomplete_fields = ('doctorant','type',)

@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('get_annee','get_doctorant','get_sujet','sujet_detail')
    list_filter = ('annee','sujet')
    search_fields = ('annee__intitule','doctorant__nom','doctorant__prenom','doctorant__cne','doctorant__cin','sujet_detail','sujet__intitule')
    autocomplete_fields = ('annee','doctorant','sujet')


    @admin.display(description='Inscription Année')
    def get_annee(self, obj):
        return obj.annee


    @admin.display(description='Doctorant')
    def get_doctorant(self, obj):
        return obj.doctorant

    @admin.display(description='Sujet')
    def get_sujet(self, obj):
        return obj.sujet

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('sujet','intitule','date','url')
    search_fields = ('intitule','description','inscription__annee__intitule','inscription__doctorant__nom','inscription__doctorant__prenom','inscription__doctorant__cne','inscription__doctorant__cin','inscription__sujet_detail','inscription__sujet__intitule')
    autocomplete_fields = ('inscription',)

@admin.register(Formation_C_Inscription)
class Formation_C_InscriptionAdmin(admin.ModelAdmin):
    list_display = ('inscription','formation_complementaire','date')
    autocomplete_fields = ('inscription','formation_complementaire')

class MemberInline(admin.TabularInline):
    model = SoutenanceMembers
    extra = 0

@admin.register(Soutenance)
class SoutenanceAdmin(admin.ModelAdmin):
    list_display = ('doctorant','date','localisation','president')
    autocomplete_fields = ('doctorant','president','localisation')
    inlines = (MemberInline,)