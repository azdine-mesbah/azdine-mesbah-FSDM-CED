from django import forms
from datetime import datetime

from Administration.models import Enseignant

from CED_Tools.tools.Constants import SEXES
from CED_Tools.models import Annee

from .models import Doctorant, Cursus, Inscription, Publication, Retrait, RetraitType, Soutenance, SoutenanceMembers

class DoctorantCreateForm(forms.ModelForm):
    class Meta:
        model = Doctorant
        fields = '__all__'
    
    photo = forms.ImageField(widget=forms.FileInput, required=False)
    sexe = forms.ChoiceField(choices=SEXES,widget=forms.RadioSelect)
    date_naissance = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"01/01/2000 ou 2000"}))
    nom_ar = forms.CharField(label='الاسم العائلي', widget=forms.TextInput(attrs={'dir':'rtl'}))
    prenom_ar = forms.CharField(label='الاسم الشخصي', widget=forms.TextInput(attrs={'dir':'rtl'}))
    lieu_naissance_ar = forms.CharField(label='مكان الازدياد', widget=forms.TextInput(attrs={'dir':'rtl'}))
    telephone = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"0612345789"}))

class CursusCreateForm(forms.ModelForm):
    class Meta:
        model = Cursus
        fields = "__all__"
        widgets = {'doctorant': forms.HiddenInput(), 'duree': forms.TextInput(), 'moyenne':forms.TextInput()}

class InscriptionCreateForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = '__all__'
        widgets = {'doctorant': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance']:
            inscriptions = kwargs['initial']['doctorant'].inscriptions.exclude(annee_id=kwargs['instance'].annee_id).values_list('annee_id')
            self.fields['annee'].queryset = Annee.objects.exclude(pk__in=inscriptions)
            self.fields['annee'].widget = forms.HiddenInput()
        else:
            inscriptions = kwargs['initial']['doctorant'].inscriptions.values_list('annee_id')
            self.fields['annee'].queryset = Annee.objects.exclude(pk__in=inscriptions)

class RetraitCreateForm(forms.ModelForm):
    class Meta:
        model = Retrait
        fields = '__all__'
        widgets = {'doctorant': forms.HiddenInput(), 'date_retour':forms.DateTimeInput(attrs={'type': 'datetime-local', 'max':datetime.now().strftime("%Y-%m-%d") })}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance']:
            retraits = kwargs['initial']['doctorant'].retraits.exclude(type_id=kwargs['instance'].type_id).values_list('type_id')
            self.fields['type'].queryset = RetraitType.objects.exclude(pk__in=retraits)
        else:
            self.fields['date_retour'].widget = forms.HiddenInput()
            retraits = kwargs['initial']['doctorant'].retraits.values_list('type_id')
            self.fields['type'].queryset = RetraitType.objects.exclude(pk__in=retraits)

class PublicationCreateForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = '__all__'
        widgets = {"date":forms.DateTimeInput(attrs={'type': 'datetime-local'})}

class SoutenanceCreateForm(forms.ModelForm):
    class Meta:
        model = Soutenance
        fields = '__all__'
        exclude = ('enseignants',)
        widgets = {'date':forms.DateTimeInput(attrs={'type': 'datetime-local'}), 'inscription':forms.HiddenInput()}
    
    directeur = forms.CharField(label='Directeur de thèse',widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        doctorant = kwargs['initial']['doctorant']
        self.fields['inscription'].initial = doctorant.inscriptions.last()
        self.fields['directeur'].queryset = Enseignant.objects.filter(pk=doctorant.inscriptions.last().sujet.directeur.pk)
        self.fields['directeur'].initial = doctorant.inscriptions.last().sujet.directeur

class SoutenanceMemberCreateForm(forms.ModelForm):
    class Meta:
        model = SoutenanceMembers
        fields = '__all__'
        widgets = {'soutenance':forms.HiddenInput(),'rapporteur':forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        soutenance = kwargs['initial']['soutenance']
        self.fields['soutenance'].initial = soutenance
        self.fields['rapporteur'].initial = kwargs['initial']['type'] == 'rapporteur'
        self.fields['member'].label = kwargs['initial']['type'].capitalize()

        excluded_members = list(soutenance.enseignants.through.objects.values_list('member_id', flat=True)) + [soutenance.president.pk, soutenance.inscription.sujet.directeur.pk]

        if 'instance' in kwargs and kwargs['instance']:
            excluded_members.remove(kwargs['instance'].member.pk)

        self.fields['member'].queryset = Enseignant.objects.exclude(pk__in=excluded_members)
