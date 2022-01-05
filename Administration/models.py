from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from CED_Tools.tools.Classes import TimeStampedModel
from CED_Tools.models import Annee, Pays


class Departement(TimeStampedModel):
    class Meta:
        db_table = 'ced_departements'

    intitule = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.intitule

class Etablissement(TimeStampedModel):
    class Meta:
        db_table = 'ced_etablissements'

    intitule = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    ville = models.CharField(max_length=255)
    pays = models.ForeignKey(Pays, on_delete=models.DO_NOTHING, related_name='etablissements')
    
    def __str__(self):
        return f"{self.intitule} ({self.ville}, {self.pays})"

class Enseignant(TimeStampedModel):
    class Meta:
        db_table = 'ced_enseignants'

    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    cin = models.CharField(max_length=50, blank=True, null=True)
    som =  models.CharField(max_length=50, blank=True, null=True)
    telephone = PhoneNumberField(blank=True, null=True)
    etablissement = models.ForeignKey(Etablissement, on_delete=models.DO_NOTHING, related_name='enseignants')

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    def get_current_laboratoire(self):
        try:
            return self.laboratoires.filter(courant=True).first().laboratoire
        except:
            return None

class FormationDoctorale(TimeStampedModel):
    class Meta:
        db_table = 'ced_formations_doctorales'
    intitule = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    acronyme = models.CharField(max_length=255)
    co_ordonateur = models.ForeignKey(Enseignant, on_delete=models.DO_NOTHING, related_name="formations_doctorales")

    def __str__(self) -> str:
        return f"({self.acronyme}) {self.intitule}"

class Laboratoire(TimeStampedModel):
    class Meta:
        db_table = 'ced_laboratoires'

    intitule = models.CharField(max_length=255)
    acronyme = models.CharField(max_length=255)
    departement = models.ForeignKey(Departement, on_delete=models.DO_NOTHING, related_name="laboratoires")
    formation_doctorale = models.ForeignKey(FormationDoctorale, on_delete=models.DO_NOTHING, related_name="laboratoires")

    def __str__(self):
        return f'({self.acronyme}) {self.intitule} -- {self.get_current_directeur()}'

    def get_current_directeur(self):
        try:
            return self.directeurs.filter(courant=True).first().directeur
        except:
            return None

class LaboratoireDirecteur(TimeStampedModel):
    class Meta:
        db_table = 'ced_laboratoire_directeur'
    directeur = models.ForeignKey(Enseignant, on_delete=models.DO_NOTHING, related_name='laboratoires')
    laboratoire = models.ForeignKey(Laboratoire, on_delete=models.DO_NOTHING, related_name='directeurs')
    courant = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.laboratoire} - {self.directeur}"

class Sujet(TimeStampedModel):

    class Meta:
        db_table = 'ced_sujets'

    annee = models.ForeignKey(Annee, on_delete=models.DO_NOTHING, related_name='sujets')
    intitule = models.CharField(max_length=255)
    laboratoire = models.ForeignKey(Laboratoire, on_delete=models.DO_NOTHING, related_name='sujets')
    directeur = models.ForeignKey(Enseignant, on_delete=models.DO_NOTHING, related_name='sujets')
    co_directeur = models.ForeignKey(Enseignant, on_delete=models.DO_NOTHING, related_name='co_sujets', null=True, blank=True)

    def __str__(self):
        return f"({self.annee}) {self.intitule}"

class TypeFormationComplementaire(TimeStampedModel):
    class Meta:
        db_table = 'ced_types_formations_complementaires'

    intitule = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.intitule

class FormationComplementaire(TimeStampedModel):
    class Meta:
        db_table = 'ced_formations_complementaires'

    type = models.ForeignKey(TypeFormationComplementaire, on_delete=models.DO_NOTHING, related_name='formations_complementaires')
    formation_doctorale = models.ForeignKey(FormationDoctorale, on_delete=models.DO_NOTHING, related_name='formations_complementaires')
    intitule = models.CharField(max_length=255)
    volume_horaire = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200)])

    def __str__(self) -> str:
        return self.intitule