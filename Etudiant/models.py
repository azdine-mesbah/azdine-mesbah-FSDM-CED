from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
from numpy import busday_count

from CED_Tools.tools.Classes import TimeStampedModel
from CED_Tools.tools.Constants import SEXES, HANDICAPE_CHOICES, SITUATIONS_FAMILIALES
from CED_Tools.tools.Functions import photo_upload_to, cv_upload_to, cursus_document_upload_to, safe_image_tag, birhdayValidator, avg_to_mention, current_year
from CED_Tools.models import Annee, Pays

from Administration.models import Sujet, FormationComplementaire, Enseignant, LocalisationSoutenance

# Create your models here.

class Doctorant(TimeStampedModel):

    class Meta:
        db_table = 'ced_doctorants'
    
    photo = models.ImageField(upload_to=photo_upload_to, max_length=255, blank=True, null=True)
    nom = models.CharField(max_length=63)
    prenom = models.CharField(max_length=63)
    sexe = models.CharField(max_length=1, choices=SEXES)
    cne = models.CharField('CNE', max_length=15)
    cin = models.CharField('CIN', max_length=15, unique=True)
    date_naissance = models.CharField('Date de naissance', max_length=10, validators=(birhdayValidator,), blank=True, null=True)
    lieu_naissance = models.CharField('Lieu de naissance', max_length=255, blank=True, null=True)
    pays = models.ForeignKey(Pays, on_delete=models.DO_NOTHING, default=Pays.default_value_id, related_name='doctorants', blank=True, null=True)
    
    nom_ar = models.CharField(max_length=127, blank=True, null=True)
    prenom_ar = models.CharField(max_length=127, blank=True, null=True)
    lieu_naissance_ar = models.CharField(max_length=255, blank=True, null=True)
    
    adresse = models.CharField(max_length=255, blank=True, null=True)
    ville = models.CharField(max_length=127, blank=True, null=True)

    telephone = PhoneNumberField(blank=True, null=True)
    email_ac = models.EmailField(verbose_name='Email Académique', blank=True, null=True)
    email_pr = models.EmailField(verbose_name='Email Personnelle', blank=True, null=True)

    cv = models.FileField(verbose_name='Curriculum Vitae', upload_to=cv_upload_to, max_length=255, blank=True, null=True)

    handicap = models.CharField(max_length=31, blank=True, null=True, choices=HANDICAPE_CHOICES)
    situation_f = models.CharField(max_length=1, blank=True, null=True, choices=SITUATIONS_FAMILIALES)

    fonctionnaire = models.BooleanField(default=False, blank=True, null=True)
    employeur = models.CharField(max_length=255, blank=True, null=True)
    profession = models.CharField(max_length=255, blank=True, null=True)

    search_indexer = models.CharField(max_length=255, blank=True, null=True)

    @property
    def email(self):
        return self.email_ac if self.email_ac else self.email_pr

    @property
    def photo_preview(self):
        return safe_image_tag(self.photo.url if self.photo else None)

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
        return self.inscriptions.order_by('-created_at').last()

    @property
    def first_inscription(self):
        return self.inscriptions.order_by('-created_at').first()

class CursusType(TimeStampedModel):
    class Meta:
        db_table = 'ced_cursus_types'
        verbose_name_plural = 'Types de Cursus'

    intitule = models.CharField(max_length=255)
    acronyme = models.CharField(max_length=63)
    description = models.CharField(max_length=255)
    duree_annees = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self) -> str:
        return f"{self.intitule} ({self.acronyme})"

    @property
    def duree(self):
        return f"{self.duree_annees} an" + ("s" if self.duree_annees > 1 else "")

class Cursus(TimeStampedModel):
    class Meta:
        db_table = 'ced_cursus'
        verbose_name_plural = 'Cursus'

    doctorant = models.ForeignKey(Doctorant, on_delete=models.DO_NOTHING, related_name='cursus')
    type = models.ForeignKey(CursusType, on_delete=models.DO_NOTHING, related_name='cursus')
    annee = models.ForeignKey(Annee, on_delete=models.DO_NOTHING, related_name='cursus', blank=True, null=True)

    intitule = models.CharField(max_length=255)
    date_obtention = models.DateField("Date d'obtention", blank=True, null=True)
    moyenne = models.DecimalField(decimal_places=2, max_digits=4, validators=[MinValueValidator(10), MaxValueValidator(20)], blank=True, null=True)
    duree = models.IntegerField(verbose_name="Durée (ans)", validators=[MinValueValidator(1)], blank=True, null=True)
    ville = models.CharField(max_length=255, blank=True, null=True)
    etablissement = models.CharField(verbose_name="Etablissement", max_length=255, blank=True, null=True)
    photo_diplome = models.FileField(verbose_name="Diplôme", upload_to=cursus_document_upload_to, max_length=255, blank=True, null=True)
    photo_releve = models.FileField(verbose_name="Relevé des notes", upload_to=cursus_document_upload_to, max_length=255, blank=True, null=True)
    

    @property
    def mention(self):
        return avg_to_mention(self.moyenne)

    @property
    def get_duree(self):
        return f"{self.duree} an" + ("s" if self.duree > 1 else "")

    def __str__(self) -> str:
        return f"{self.type} - {self.intitule}"

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
    sujet_detail = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"({self.annee}) {self.sujet} -- {self.doctorant}"

    @property
    def date(self):
        return self.created_at.strftime("%d/%m/%Y") 

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
    speciality = models.CharField('spécialité', max_length=255, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    localisation = models.ForeignKey(LocalisationSoutenance, on_delete=models.DO_NOTHING, related_name='soutenances', blank=True, null=True)
    president = models.ForeignKey(Enseignant, on_delete=models.DO_NOTHING, related_name='soutenances')
    enseignants = models.ManyToManyField(Enseignant, through='SoutenanceMembers')

    @property
    def rapporteurs(self):
        return self.enseignants.through.objects.filter(rapporteur=True)

    @property
    def members(self):
        return self.enseignants.through.objects.filter(rapporteur=False)

    @property
    def doctorant_email(self):
        return self.emails.filter(address=self.doctorant.email).first()

    @property
    def president_email(self):
        return self.emails.filter(address=self.president.email).first()
    
    @property
    def directeur_email(self):
        return self.emails.filter(address=self.doctorant.last_inscription.sujet.directeur.email).first()

    @property
    def co_directeur_email(self):
        return self.emails.filter(address=self.doctorant.last_inscription.sujet.co_directeur.email).first()

class SoutenanceMembers(TimeStampedModel):
    class Meta:
        db_table = 'ced_soutenence_members'

    soutenance = models.ForeignKey(Soutenance, on_delete=models.DO_NOTHING)
    member = models.ForeignKey(Enseignant, on_delete=models.DO_NOTHING)
    rapporteur = models.BooleanField(default=False)
    emailed = models.BooleanField(default=False)

    @property
    def invitation_email(self):
        return self.soutenance.emails.filter(address=self.member.email, type="invitation").first()

    @property
    def rapport_email(self):
        return self.soutenance.emails.filter(address=self.member.email, type="rapport").first()

class SoutenanceEmail(TimeStampedModel):
    class Meta:
        db_table = 'ced_soutenance_emails'

    soutenance = models.ForeignKey(Soutenance, on_delete=models.DO_NOTHING, related_name='emails')
    type = models.CharField(max_length=255, null=True)
    address = models.EmailField()
    sended = models.BooleanField(default=False)
    error_message = models.CharField(max_length=255, null=True)