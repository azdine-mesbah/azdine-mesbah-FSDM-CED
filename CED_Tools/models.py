from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _
from django.utils.html import mark_safe
from humanize import naturalsize

from .tools.Classes import TimeStampedModel
from .tools.Functions import file_upload_to


class Annee(TimeStampedModel):
    class Meta:
        db_table = 'ced_annees'
        verbose_name_plural = 'Années Scolaires'
        ordering = ['-annee']
    
    annee = models.IntegerField()

    def __str__(self):
        return f"{self.annee}"

    @property
    def intitule(self):
        return f"{self.annee}/{self.annee+1}"

class Pays(TimeStampedModel):
    # table name
    class Meta:
        db_table = 'ced_pays'
        verbose_name_plural = 'Pays'

    # attributes
    nom = models.CharField(max_length=255)

    # methodes
    def __str__(self) -> str:
        return self.nom

    @staticmethod
    def default_value_id():
        try:
            return Pays.objects.get(nom = "Maroc").pk
        except:
            return -1

class BulkData(TimeStampedModel):
    class Meta:
        db_table = 'ced_fichers'
        verbose_name_plural = 'Fichiers'
    file = models.FileField(upload_to=file_upload_to)
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)

    @property
    def file_name(self):
        return self.file.name.split('_-_')[-1]
    
    @property
    def file_size(self):
        return naturalsize(self.file.size)

    @property
    def download_link(self):
        return mark_safe(f'<a href="{self.file.url}">'+_('Download')+'</a>')

    def get_content_type_fields(self):
        excluded_fields = ['id'] + list(map(lambda x:x.name, TimeStampedModel._meta.fields))
        model_fields = self.content_type.model_class()._meta.fields
        managed_fields = [field for field in model_fields if field.name not in excluded_fields]
        return managed_fields
