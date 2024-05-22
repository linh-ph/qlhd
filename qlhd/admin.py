from django.contrib import admin
from .models import *


class DistributorAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'tax_code')
    search_fields = ['name', 'phone']
    list_filter = ('name',)


admin.site.register(Distributor, DistributorAdmin)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('distributor_id', 'code_bill', 'date_invoice', 'total_money', 'total_tax', 'total')
    search_fields = ['code_bill']
    list_filter = ('code_bill',)


admin.site.register(Invoice, InvoiceAdmin)


class DetailInvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_id', 'name', 'unit', 'quantity', 'price', 'total_price', 'tax', 'total')
    search_fields = ['name']
    list_filter = ('name',)


admin.site.register(DetailInvoice, DetailInvoiceAdmin)

admin.site.register(Purchaser)
