from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


def upload_path(instance, filename):
    return '/'.join(['upload', str(instance.folder), filename])


def get_id(self):
    return str(self.id)


User.add_to_class("__str__", get_id)


class Distributor(models.Model):
    name = models.CharField(max_length=100, default=None, blank=True)
    address = models.CharField(max_length=100, default=None, blank=True)
    tax_code = models.CharField(max_length=100, default=None, blank=True)
    phone = models.CharField(max_length=100, default=None, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class Purchaser(models.Model):
    name_buyer = models.CharField(max_length=100, default=None, blank=True)
    company = models.CharField(max_length=100, default=None, blank=True)
    address = models.CharField(max_length=100, default=None, blank=True)
    phone = models.CharField(max_length=100, default=None, blank=True)
    tax_code = models.CharField(max_length=100, default=None, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class TaxInvoice(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    distributor_id = models.ForeignKey(Distributor, on_delete=models.CASCADE, null=True)
    purchaser_id = models.ForeignKey(Purchaser, on_delete=models.CASCADE, null=True)
    bill_of_lading_no = models.CharField(max_length=100, default=None, blank=True, null=True)
    code_bill = models.CharField(max_length=100, default=None, blank=True, null=True)
    image_path = models.CharField(max_length=100, default=None, blank=True, null=True)
    form_of_payment = models.CharField(max_length=100, null=True, default=None, blank=True)
    date_invoice = models.CharField(max_length=100, null=True, default=None, blank=True)
    total_money = models.CharField(max_length=100, null=True, default=None, blank=True)
    total_tax = models.CharField(max_length=100, null=True, default=None, blank=True)
    total = models.CharField(max_length=100, null=True, default=None, blank=True)
    status = models.CharField(max_length=100, null=True, default=None, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class DetailInvoice(models.Model):
    tax_invoice_id = models.ForeignKey(TaxInvoice, on_delete=models.CASCADE, null=True)
    unit = models.CharField(max_length=100, null=True, default=None, blank=True)
    quantity = models.CharField(max_length=100, null=True, default=None, blank=True)
    price = models.CharField(max_length=100, null=True, default=None, blank=True)
    total_price = models.CharField(max_length=100, null=True, default=None, blank=True)
    tax = models.CharField(max_length=100, null=True, default=None, blank=True)
    tax_money = models.CharField(max_length=100, null=True, default=None, blank=True)
    total = models.CharField(max_length=100, null=True, default=None, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class Product(models.Model):
    detail_invoice_id = models.ForeignKey(DetailInvoice, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True, default=None, blank=True)
    unit = models.CharField(max_length=100, null=True, default=None, blank=True)
    type = models.CharField(max_length=100, null=True, default=None, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
