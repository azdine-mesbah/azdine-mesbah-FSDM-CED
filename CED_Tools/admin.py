from django.contrib import admin
from django.contrib.auth.models import Permission

from .models import Annee, Pays #, BulkData
# from .forms import BulkDataCreateForm
# Register your models here.

admin.site.register(Permission)

@admin.register(Annee)
class AnneeAdmin(admin.ModelAdmin):
    list_display = ('annee','intitule')
    search_fields = ('annee',)

@admin.register(Pays)
class PaysAdmin(admin.ModelAdmin):
    search_fields = ('nom',)

# @admin.register(BulkData)
# class BulkDataAdmin(admin.ModelAdmin):
#     list_display = ('content_type','file_name','file_size','download_link')
#     form = BulkDataCreateForm
