from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext as _
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime

from CED_Tools.tools.Classes import TimeStampedModel
from CED_Tools.tools.Constants import SEXES, MENTIONS
from CED_Tools.tools.Functions import photo_upload_to, safe_image_tag, birhdayValidator, avg_to_mention, current_year
from CED_Tools.models import Annee, Pays

from Administration.models import Sujet

# Create your models here.

class Doctorant(TimeStampedModel):

    class Meta:
        db_table = 'ced_doctorants'
    
    photo = models.ImageField(upload_to=photo_upload_to, blank=True, null=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    sexe = models.CharField(max_length=1, choices=SEXES)
    cne = models.CharField('CNE',max_length=10)
    cin = models.CharField('CIN',max_length=10)
    date_naissance = models.CharField('Date de naissance', max_length=10, validators=(birhdayValidator,))
    lieu_naissance = models.CharField('Lieu de naissance', max_length=255)
    pays = models.ForeignKey(Pays, on_delete=models.DO_NOTHING, default=Pays.default_value_id)
    nom_ar = models.CharField(max_length=100)
    prenom_ar = models.CharField(max_length=100)
    lieu_naissance_ar = models.CharField(max_length=255)
    
    adresse = models.CharField(max_length=255, blank=True, null=True)
    ville = models.CharField(max_length=100)

    telephone = PhoneNumberField(blank=True, null=True)
    email_ac = models.EmailField(max_length=255, blank=True, null=True, )
    email_pr = models.EmailField(max_length=255, blank=True, null=True, )

    handicap = models.BooleanField(default=False)

    annee_bac = models.ForeignKey(Annee, on_delete=models.DO_NOTHING)
    centre_bac = models.CharField(max_length=255)
    mention_bac = models.CharField(max_length=10, choices=MENTIONS)
    academie_bac = models.CharField(max_length=255)
    serie_bac = models.CharField(max_length=16)

    fonctionnaire = models.BooleanField(default=False)
    employeur = models.CharField(max_length=255, blank=True, null=True)
    profession = models.CharField(max_length=255, blank=True, null=True)

    @property
    def photo_preview(self):
        return safe_image_tag(self.photo.url) if self.photo else safe_image_tag()

    def __str__(self) -> str:
        return f"{self.cin.upper()} - {self.nom.upper()} {self.prenom.upper()}"

class CursusType(TimeStampedModel):
    class Meta:
        db_table = 'ced_cursus_types'
        verbose_name_plural = 'Types de Cursus'

    intitule = models.CharField(max_length=255)
    duree_annees = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.intitule} - ({self.duree})"

    @property
    def duree(self):
        return f"{self.duree_annees} an" + ("s" if self.duree_annees > 1 else "")

class Cursus(TimeStampedModel):
    class Meta:
        db_table = 'ced_cursus'
        verbose_name_plural = 'Cursus'

    doctorant = models.ForeignKey(Doctorant, on_delete=models.DO_NOTHING, related_name='cursus')
    type = models.ForeignKey(CursusType, on_delete=models.DO_NOTHING, related_name='cursus')
    annee = models.ForeignKey(Annee, on_delete=models.DO_NOTHING, related_name='cursus')
    specialite = models.CharField(max_length=255)
    duree = models.IntegerField(validators=[MinValueValidator(1)])
    ville = models.CharField(max_length=255)
    etablissement = models.CharField(max_length=255)
    moyenne = models.DecimalField(decimal_places=2, max_digits=4, validators=[MinValueValidator(10), MaxValueValidator(20)])

    @property
    def mention(self):
        return avg_to_mention(self.moyenne)

    @property
    def get_duree(self):
        return f"{self.duree} an" + "s" if self.duree > 1 else ""

    def __str__(self) -> str:
        return f"{self.type} - {self.specialite}"

class RetraitType(TimeStampedModel):
    class Meta:
        db_table = 'ced_retraits_types'
        verbose_name_plural = 'Types de documents à retirer'
    
    intitule = models.CharField(max_length=255)
    max_delais = models.IntegerField("Délais Maximum", default=3)

    def __str__(self):
        return self.intitule
        
class Retrait(TimeStampedModel):
    class Meta:
        db_table = 'ced_retraits'
        verbose_name_plural = 'Retraits'
    
    type = models.ForeignKey(RetraitType, on_delete=models.DO_NOTHING, related_name='retraits')
    doctorant = models.ForeignKey(Doctorant, on_delete=models.DO_NOTHING, related_name='retraits')
    created_at = models.DateTimeField('date création', auto_now_add=True)
    date_retour = models.DateTimeField(blank=True, null=True)
    definitif = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.type} par {self.doctorant}"

    def delay(self):
        return (datetime.now().date() - self.created_at.date()).days - 1

    def is_late(self):
        return self.delay() > 0

    def return_date(self):
        if self.definitif:
            return _('Definitive Withdrawal')
        elif self.date_retour:
            return self.date_retour
        elif self.is_late():
            return f"{_('Late by')} : {self.delay()} {_('Days')}"
        else:
            return "--"
     
class Inscription(TimeStampedModel):
    class Meta:
        db_table = 'ced_inscriptions'

    doctorant = models.ForeignKey(Doctorant, on_delete=models.DO_NOTHING, related_name='inscriptions')
    annee = models.ForeignKey(Annee, on_delete=models.DO_NOTHING, related_name='inscriptions', default=current_year)
    sujet = models.ForeignKey(Sujet, on_delete=models.DO_NOTHING, related_name='inscriptions')
    sujet_detail = models.CharField(max_length=255)
