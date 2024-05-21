from django import forms
# from qlhd.models import Image


class StoreForm(forms.ModelForm):
    url = forms.ImageField(label=(), required=True, error_messages={
        'required': 'Clear ',
    })

    # class Meta:
    #     model = Image
    #     fields = ['url']
