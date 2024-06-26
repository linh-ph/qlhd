from django import forms
from django.contrib.auth.models import User
from qlhd import models


class CustomerUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ['address', 'mobile', 'profile_pic']


class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = ['name', 'price', 'description', 'product_image', 'unit', 'type']


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = models.Invoice
        fields = '__all__'


class AddressForm(forms.Form):
    Email = forms.EmailField()
    Mobile = forms.IntegerField()
    Address = forms.CharField(max_length=500)


class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Orders
        fields = ['status']


class DistributorForm(forms.ModelForm):
    class Meta:
        model = models.Distributor
        fields = '__all__'


class DetailInvoiceForm(forms.ModelForm):
    class Meta:
        model = models.DetailInvoice
        fields = '__all__'
