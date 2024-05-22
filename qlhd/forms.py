from django import forms
from .models import Distributor


class DistributorForm(forms.ModelForm):
    url = forms.ImageField(label=(''), required=True, error_messages={
        'required': 'Clear ',
    })

    class Meta:
        model = Distributor
        fields = ['url']
