from django import forms
from django.core.exceptions import ValidationError
from .models import Laboratoire, Enseignant, LaboratoireDirecteur, Sujet


class LaboratoireCreateForm(forms.ModelForm):
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
        

class SujetCreateForm(forms.ModelForm):
    class Meta:
        model = Sujet
        fields = '__all__'

    co_directeur = forms.ModelChoiceField(queryset=None, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        if 'instance' in kwargs and kwargs['instance']:
            print(kwargs['instance'].co_directeur)
            self.fields['co_directeur'].queryset = Enseignant.objects.exclude(pk=kwargs['instance'].directeur.pk)
            self.fields['co_directeur'].initial = kwargs['instance'].co_directeur
        else:
            self.fields['co_directeur'].queryset = Enseignant.objects.all()

    def clean(self):
        if self.cleaned_data['co_directeur'] == self.cleaned_data['laboratoire'].get_current_directeur():
            raise ValidationError('Le Directeur et le Co-Directeur ne doivent pas être les même. (vous pouvez laissier vide!)')
        return super().clean()
            
        