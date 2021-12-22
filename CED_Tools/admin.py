from django.contrib import admin
from django.contrib.auth.models import Permission

from .models import Annee, Pays
# Register your models here.

admin.site.register(Permission)

@admin.register(Annee)
class AnneeAdmin(admin.ModelAdmin):
    list_display = ('annee','intitule')
    search_fields = ('annee',)

@admin.register(Pays)
class PaysAdmin(admin.ModelAdmin):
    search_fields = ('nom',)
