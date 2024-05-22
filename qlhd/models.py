from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


def upload_path(instance, filename):
    return '/'.join(['upload', str(instance.folder), filename])


def get_id(self):
    return str(self.id)


User.add_to_class("__str__", get_id)


class Distributor(models.Model):
    name = models.CharField(max_length=100, default=None, null=True)
    address = models.CharField(max_length=100, default=None, null=True)
    tax_code = models.CharField(max_length=100, default=None, null=True)
    phone = models.CharField(max_length=100, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class Purchaser(models.Model):
    name_buyer = models.CharField(max_length=100, default=None, null=True)
    company = models.CharField(max_length=100, default=None, null=True)
    address = models.CharField(max_length=100, default=None, null=True)
    phone = models.CharField(max_length=100, default=None, null=True)
    tax_code = models.CharField(max_length=100, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class Invoice(models.Model):
    created = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    distributor = models.ForeignKey(Distributor, on_delete=models.CASCADE, null=True)
    purchaser = models.ForeignKey(Purchaser, on_delete=models.CASCADE, null=True)

    bill_of_lading_no = models.CharField(max_length=100, default=None, null=True)
    code_bill = models.CharField(max_length=100, default=None, null=True)
    image_path = models.CharField(max_length=100, default=None, null=True)
    form_of_payment = models.CharField(max_length=100, null=True, default=None)
    date_invoice = models.CharField(max_length=100, null=True, default=None)
    total_money = models.CharField(max_length=100, null=True, default=None)
    total_tax = models.CharField(max_length=100, null=True, default=None)
    total = models.CharField(max_length=100, null=True, default=None)
    status = models.CharField(max_length=100, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class DetailInvoice(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True, default=None)
    unit = models.CharField(max_length=100, null=True, default=None)
    quantity = models.CharField(max_length=100, null=True, default=None)
    price = models.CharField(max_length=100, null=True, default=None)
    total_price = models.CharField(max_length=100, null=True, default=None)
    tax = models.CharField(max_length=100, null=True, default=None)
    tax_money = models.CharField(max_length=100, null=True, default=None)
    total = models.CharField(max_length=100, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class Product(models.Model):
    name = models.CharField(max_length=100, null=True, default=None)
    unit = models.CharField(max_length=100, null=True, default=None)
    type = models.CharField(max_length=100, null=True, default=None)
    product_image = models.CharField(max_length=100, null=True, default=None)
    price = models.CharField(max_length=100, null=True, default=None)
    description = models.CharField(max_length=100, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    profile_pic = models.ImageField(upload_to='profile_pic/CustomerProfilePic/', null=True, blank=True)
    address = models.CharField(max_length=40, null=True)
    mobile = models.CharField(max_length=20, null=True)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.first_name


class Orders(models.Model):
    STATUS = (
        ('Đang giao', 'Pending'),
        ('Xác nhận đơn hàng', 'Order Confirmed'),
        ('Đang giao hàng', 'Delivering'),
        ('Đã giao hàng', 'Delivered'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    email = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=500, null=True)
    mobile = models.CharField(max_length=20, null=True)
    order_date = models.DateField(auto_now_add=True, null=True)
    status = models.CharField(max_length=50, null=True, choices=STATUS)


class OrdersDetail(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    price = models.CharField(max_length=40, null=True)

    def __str__(self):
        return self.name


class Feedback(models.Model):
    name = models.CharField(max_length=40, null=True)
    feedback = models.CharField(max_length=500, null=True)
    date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
