from django import forms
from django.core.exceptions import ValidationError
from .models import Departement, FormationComplementaire, FormationDoctorale, Laboratoire, Enseignant, LaboratoireDirecteur, Sujet

class DepartmentCreateForm(forms.ModelForm):
    class Meta:
        model = Departement
        fields = '__all__'

class LaboratoireAdminCreateForm(forms.ModelForm):
    class Meta:
        model = Laboratoire
        fields = '__all__'
    directeur = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance']:
            current_directeurs = LaboratoireDirecteur.objects.filter(courant=True).exclude(laboratoire_id=kwargs['instance'].pk)
            self.fields['directeur'].initial = kwargs['instance'].get_current_directeur()
        else:
            current_directeurs = LaboratoireDirecteur.objects.filter(courant=True)
        self.fields['directeur'].queryset = Enseignant.objects.exclude(pk__in=[_.directeur_id for _ in current_directeurs])

    def save(self, commit: bool = ...):
        laboratoire = super().save(commit=commit)
        laboratoire.save()
        # creating m2m relationship with directeur
        directeur = self.cleaned_data['directeur']
        directeur.laboratoires.filter(courant=True).update(courant=False)
        laboratoire.directeurs.filter(courant=True).update(courant=False)
        laboratoire.directeurs.create(directeur_id = directeur.id)
        return laboratoire

class LaboratoireCreateForm(LaboratoireAdminCreateForm):
    class Meta:
        model = Laboratoire
        fields = '__all__'
        widgets = {'departement': forms.HiddenInput()}

class SujetAdminCreateForm(forms.ModelForm):
    class Meta:
        model = Sujet
        fields = '__all__'

    co_directeur = forms.ModelChoiceField(queryset=None, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.fields['co_directeur'].queryset = Enseignant.objects.all()
        if 'instance' in kwargs and kwargs['instance']:
            self.fields['co_directeur'].queryset = Enseignant.objects.exclude(pk=kwargs['instance'].directeur.pk)
            self.fields['co_directeur'].initial = kwargs['instance'].co_directeur
        elif 'initial' in kwargs and kwargs['initial']:
            self.fields['co_directeur'].queryset = Enseignant.objects.exclude(pk=kwargs['initial']['directeur'].pk)

    def clean(self):
        if self.cleaned_data['co_directeur'] == self.cleaned_data['directeur']:
            raise ValidationError('Le Directeur de thèse et le Co-Directeur ne doivent pas être les même. (vous pouvez laissier vide!)')
        # elif self.cleaned_data['laboratoire'].get_current_directeur() != self.cleaned_data['directeur']:
        #     raise ValidationError('Directeur and Laboratoire missmatch')
        return super().clean()

class SujetCreateForm(SujetAdminCreateForm):
    class Meta:
        model = Sujet
        fields = '__all__'
        widgets = {'directeur':forms.HiddenInput(), 'intitule':forms.Textarea(attrs={'rows':4})}

class FormationDoctoraleCreateForm(forms.ModelForm):
    class Meta:
        model = FormationDoctorale
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_coordenateurs = FormationDoctorale.objects.all()
        if 'instance' in kwargs and kwargs['instance']:
            current_coordenateurs = current_coordenateurs.exclude(pk=kwargs['instance'].pk)
            self.fields['co_ordonateur'].initial = kwargs['instance'].co_ordonateur
        self.fields['co_ordonateur'].queryset = Enseignant.objects.exclude(pk__in=[_.co_ordonateur_id for _ in current_coordenateurs])

class FormationComplementaireCreateForm(forms.ModelForm):
    class Meta:
        model = FormationComplementaire
        fields = '__all__'
        widgets = {'formation_doctorale': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance']:
            pass
        else:
            self.fields['formation_doctorale'].initial = self.initial['formation']