from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime
from qlhd.models import Distributor


def upload_path(instance, filename):
    return '/'.join(['upload', str(instance.folder), filename])


def get_id(self):
    return str(self.id)


User.add_to_class("__str__", get_id)


# class Session(models.Model):
#     id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
#     folder = models.CharField(max_length=100, default=None, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return str(self.id)


# class Distributor(models.Model):
#     shop_code = models.CharField(max_length=100, default=None, blank=True, null=True)
#     code_bill = models.CharField(max_length=100, default=None, blank=True, null=True)
#     path = models.CharField(max_length=100, default=None, blank=True, null=True)
#     name_distributor = models.CharField(max_length=100, null=True, default=None, blank=True)
#     date_invoice = models.CharField(max_length=100, null=True, default=None, blank=True)
#     total_money = models.CharField(max_length=100, null=True, default=None, blank=True)
#     url = models.ImageField(upload_to=upload_path)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return str(self.id)


class Product:
    id_distributor = models.ForeignKey(Distributor, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True, default=None, blank=True)
    unit = models.CharField(max_length=100, null=True, default=None, blank=True)
    quantity = models.CharField(max_length=100, null=True, default=None, blank=True)
    price = models.CharField(max_length=100, null=True, default=None, blank=True)
    total_price = models.CharField(max_length=100, null=True, default=None, blank=True)
    tax = models.CharField(max_length=100, null=True, default=None, blank=True)
    money_tax = models.CharField(max_length=100, null=True, default=None, blank=True)
    total = models.CharField(max_length=100, null=True, default=None, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Image:
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    url = models.CharField(max_length=100, null=True, default=None, blank=True)
    name = models.CharField(max_length=100, null=True, default=None, blank=True)
    upload = models.DateTimeField(default=datetime.now, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class InfoImage:
    # id_image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)
    label = models.CharField(max_length=100, null=True, default=None, blank=True)
    text = models.CharField(max_length=255, null=True, default=None, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
