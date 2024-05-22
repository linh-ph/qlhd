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
        fields = ['name', 'price', 'description', 'product_image']


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = models.Invoice
        fields = ['code_bill', 'image_path', 'form_of_payment', 'date_invoice', 'total_money', 'total_tax', 'total',
                  'status']


class AddressForm(forms.Form):
    Email = forms.EmailField()
    Mobile = forms.IntegerField()
    Address = forms.CharField(max_length=500)


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = models.Feedback
        fields = ['name', 'feedback']


class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Orders
        fields = ['status']
