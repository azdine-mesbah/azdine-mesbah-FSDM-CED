from django.db import models
from .tools.Classes import TimeStampedModel

class Annee(TimeStampedModel):
    class Meta:
        db_table = 'ced_annees'
        verbose_name_plural = 'Années Scolaires'
    
    annee = models.IntegerField()

    def __str__(self):
        return f"{self.annee}"

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
