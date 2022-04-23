from django import forms
from datetime import datetime
from django.core.exceptions import ValidationError

from Administration.models import Enseignant, LocalisationSoutenance, Sujet

from CED_Tools.tools.Constants import SEXES
from CED_Tools.models import Annee

from .models import Doctorant, Cursus, Inscription, Publication, Retrait, RetraitType, Soutenance, SoutenanceMembers

class DoctorantCreateForm(forms.ModelForm):
    class Meta:
        model = Doctorant
        fields = '__all__'
    
    photo = forms.ImageField(widget=forms.FileInput, required=False)
    sexe = forms.ChoiceField(choices=SEXES, widget=forms.RadioSelect)
    date_naissance = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"01/01/2000 ou 2000"}), required=False)
    nom_ar = forms.CharField(label='الاسم العائلي', widget=forms.TextInput(attrs={'dir':'rtl'}), required=False)
    prenom_ar = forms.CharField(label='الاسم الشخصي', widget=forms.TextInput(attrs={'dir':'rtl'}), required=False)
    lieu_naissance_ar = forms.CharField(label='مكان الازدياد', widget=forms.TextInput(attrs={'dir':'rtl'}), required=False)
    telephone = forms.CharField(label='Téléphone', widget=forms.TextInput(attrs={"placeholder":"0612345789"}), required=False)
    cv = forms.FileField(label="Curriculum Vitae", widget=forms.FileInput(attrs={'accept':'application/pdf ,image/*'}), required=False)


class CursusCreateForm(forms.ModelForm):
    class Meta:
        model = Cursus
        fields = "__all__"
        widgets = {
            'doctorant': forms.HiddenInput(),
            'duree': forms.TextInput(),
            'moyenne':forms.TextInput(attrs={'type': 'number', 'min':'10.00', 'max':'20.00', 'step':'0.01','placeholder': '12.34'}),
            'date_obtention':forms.TextInput(attrs={'type': 'date'}),
            'etablissement':forms.TextInput(attrs={'placeholder': 'Faculté des Sciences Dhar el Mahraz'}),
            'photo_diplome':forms.FileInput(attrs={'accept':'application/pdf ,image/*'}),
            'photo_releve':forms.FileInput(attrs={'accept':'application/pdf ,image/*'}),
        }

class InscriptionCreateForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = '__all__'
        widgets = {'doctorant': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        doctorant = kwargs['initial']['doctorant']
        if doctorant.soutenance:
            raise ValidationError(f'Le doctorant {doctorant} est deja fait une soutenance et il n\'a pas encore le droit de faire une inscription')
        available_sujets = [sujet.id for sujet in Sujet.objects.all() if sujet.is_available]
        if 'instance' in kwargs and kwargs['instance']:
            inscriptions = doctorant.inscriptions.exclude(annee_id=kwargs['instance'].annee_id).values_list('annee_id')
            self.fields['annee'].queryset = Annee.objects.exclude(pk__in=inscriptions)
            self.fields['annee'].widget = forms.HiddenInput()
            if not kwargs['instance'].sujet.pk in available_sujets:
                available_sujets.append(kwargs['instance'].sujet.pk)
        else:
            inscriptions = doctorant.inscriptions.values_list('annee_id')
            self.fields['annee'].queryset = Annee.objects.exclude(pk__in=inscriptions)
        self.fields['sujet'].queryset = Sujet.objects.filter(pk__in=available_sujets).order_by('intitule')

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
    date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'})
)  

class SoutenanceCreateForm(forms.ModelForm):
    class Meta:
        model = Soutenance
        fields = '__all__'
        exclude = ('enseignants',)
        widgets = {'doctorant':forms.HiddenInput(), 'date':forms.HiddenInput(), 'localisation':forms.HiddenInput()}

    directeur = forms.CharField(label='Directeur de thèse', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    co_directeur = forms.CharField(label='Co-Directeur', widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        doctorant = kwargs['initial']['doctorant']
        self.fields['doctorant'].initial = doctorant
        self.fields['directeur'].initial = doctorant.last_inscription.sujet.directeur
        self.fields['co_directeur'].initial = doctorant.last_inscription.sujet.co_directeur
        if 'instance' in kwargs and kwargs['instance']:
            self.fields['date'] = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'},), input_formats=('%Y-%m-%dT%H:%M:%S',), required=False)
            self.fields['localisation'] = forms.ModelChoiceField(queryset=LocalisationSoutenance.objects.all(), required=False)
            if kwargs['instance'].date:
                self.initial['date'] = kwargs['instance'].date.strftime('%Y-%m-%dT%H:%M:%S')
            self.initial['localisation'] = kwargs['instance'].localisation

class SoutenanceMemberCreateForm(forms.ModelForm):
    class Meta:
        model = SoutenanceMembers
        fields = '__all__'
        widgets = {'soutenance':forms.HiddenInput(),'rapporteur':forms.HiddenInput(),'emailed':forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        doctorant = kwargs['initial']['doctorant']
        soutenance = doctorant.soutenance
        self.fields['soutenance'].initial = soutenance
        self.fields['rapporteur'].initial = kwargs['initial']['type'] == 'rapporteur'
        self.fields['member'].label = kwargs['initial']['type'].capitalize()

        excluded_members = list(soutenance.enseignants.through.objects.values_list('member_id', flat=True)) + [soutenance.president.pk, doctorant.last_inscription.sujet.directeur.pk]

        if 'instance' in kwargs and kwargs['instance']:
            excluded_members.remove(kwargs['instance'].member.pk)

        self.fields['member'].queryset = Enseignant.objects.exclude(pk__in=excluded_members)
