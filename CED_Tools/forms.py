from django import forms
from .models import BulkData
class BulkDataCreateForm(forms.ModelForm):
    class Meta:
        model = BulkData
        fields = '__all__'
        widgets = {'file':forms.FileInput(attrs={'accept':'text/csv, application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}),}
