from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
from numpy import busday_count

from CED_Tools.tools.Classes import TimeStampedModel
from CED_Tools.tools.Constants import SEXES, MENTIONS
from CED_Tools.tools.Functions import photo_upload_to, safe_image_tag, birhdayValidator, avg_to_mention, current_year
from CED_Tools.models import Annee, Pays

from Administration.models import Sujet, FormationComplementaire, Enseignant, LocalisationSoutenance

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
    pays = models.ForeignKey(Pays, on_delete=models.DO_NOTHING, default=Pays.default_value_id, related_name='doctorants')
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

    @property
    def soutenance(self):
        try:
            return self.soutenances.first()
        except:
            return None

    @property
    def last_inscription(self):
        return self.inscriptions.last()

class CursusType(TimeStampedModel):
    class Meta:
        db_table = 'ced_cursus_types'
        verbose_name_plural = 'Types de Cursus'

    intitule = models.CharField(max_length=255)
    duree_annees = models.IntegerField(validators=[MinValueValidator(1)])

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

    @property
    def delay(self):
        return busday_count(self.created_at.date(), datetime.now().date()) - self.type.max_delais - 1

    @property
    def is_late(self):
        return self.delay > 0

    def return_date(self):
        if self.definitif:
            return 'Retrait définitif'
        elif self.date_retour:
            return self.date_retour
        elif self.is_late:
            return f"En retard par : {self.delay} {'jours' if self.delay > 1 else 'jour'}"
        else:
            return "--"
     
class Inscription(TimeStampedModel):
    class Meta:
        db_table = 'ced_inscriptions'

    doctorant = models.ForeignKey(Doctorant, on_delete=models.DO_NOTHING, related_name='inscriptions')
    annee = models.ForeignKey(Annee, on_delete=models.DO_NOTHING, related_name='inscriptions', default=current_year)
    sujet = models.ForeignKey(Sujet, on_delete=models.DO_NOTHING, related_name='inscriptions')
    sujet_detail = models.CharField(max_length=255)

    def __str__(self):
        return f"({self.annee}) {self.sujet} -- {self.doctorant}"

class Formation_C_Inscription(TimeStampedModel):
    class Meta:
        db_table = 'ced_fc_inscription'

    inscription = models.ForeignKey(Inscription, on_delete=models.DO_NOTHING, related_name='fomations_complementaires')
    formation_complementaire = models.ForeignKey(FormationComplementaire, on_delete=models.DO_NOTHING, related_name='inscriptions')
    date = models.DateField(blank=True, null=True)

class Publication(TimeStampedModel):
    class Meta:
        db_table = 'ced_publications'
    
    inscription =  models.ForeignKey(Inscription, on_delete=models.DO_NOTHING, related_name='publications')
    intitule = models.CharField(max_length=255)
    description = models.CharField(max_length=255,blank=True, null=True)
    url = models.CharField(max_length=255,blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    @property
    def sujet(self):
        return self.intitule

class Soutenance(TimeStampedModel):
    class Meta:
        db_table = 'ced_soutenances'

    doctorant = models.ForeignKey(Doctorant, on_delete=models.DO_NOTHING, related_name='soutenances')
    date = models.DateTimeField(blank=True, null=True)
    localisation = models.ForeignKey(LocalisationSoutenance, on_delete=models.DO_NOTHING, related_name='soutenances')
    president = models.ForeignKey(Enseignant, on_delete=models.DO_NOTHING, related_name='soutenances')
    enseignants = models.ManyToManyField(Enseignant, through='SoutenanceMembers')

    @property
    def rapporteurs(self):
        return self.enseignants.through.objects.filter(rapporteur=True)

    @property
    def members(self):
        return self.enseignants.through.objects.filter(rapporteur=False)

class SoutenanceMembers(TimeStampedModel):
    class Meta:
        db_table = 'ced_soutenence_members'

    soutenance = models.ForeignKey(Soutenance, on_delete=models.DO_NOTHING)
    member = models.ForeignKey(Enseignant, on_delete=models.DO_NOTHING)
    rapporteur = models.BooleanField(default=False)