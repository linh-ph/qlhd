from django import forms
# from api.models import Distributor
from qlhd.models import Distributor
import re
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput


class DistributorForm(forms.ModelForm):
    url = forms.ImageField(label=(''), required=True, error_messages={
        'required': 'Clear ',
    })

    class Meta:
        model = Distributor
        fields = ['url']


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Tài khoản', max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}))
    password1 = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Create password'}))
    password2 = forms.CharField(label='Nhập lại mật khẩu', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Repeat password'}))

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2 and password1:
                return password2
        raise forms.ValidationError("Mật khẩu không hợp lệ")

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+', username):
            raise forms.ValidationError("Tên tài khoản có kí tự đặc biệt")
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("Tài khoản đã tồn tại")

    def save(self):
        User.objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'],
                                 password=self.cleaned_data['password1'], is_staff=True)

        # class Meta:
        #     model = User
        #     fields = ['id', 'ip', 'port']
        #     widgets = {
        #         'name': TextInput(attrs={'class': 'form-control'}),
        #         'ip': TextInput(attrs={'class': "form-control"}),
        #         'port': TextInput(attrs={'class': 'form-control'}),
        #     }
