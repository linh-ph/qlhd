from django.contrib import admin
# Register your models here.
from .models import *
from django.http import HttpResponse
import csv

admin.site.site_header = "OCR ADMIN CMS"


def export(meta, queryset):
    field_names = [field.name for field in meta.fields]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response


# Register your models here.
class DistributorAdmin(admin.ModelAdmin):
    list_display = ['id', 'code_bill', 'shop_code', 'path', 'name_distributor', 'date_invoice',
                    'total_money', 'url']
    list_filter = ['id', 'code_bill', 'shop_code', 'path', 'name_distributor', 'date_invoice',
                   'total_money']
    search_fields = ['id', 'shop_code', 'code_bill', 'name_distributor', 'date_invoice', 'total_money']
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        return export(self.model._meta, queryset)

    export_as_csv.short_description = "Export Selected"


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'id_distributor', 'name', 'unit', 'quantity', 'price', "total_price", "tax", "money_tax", "total"]
    list_filter = ['id', 'id_distributor', 'name', 'unit', 'quantity', 'price', "total_price", "tax", "money_tax", "total"]
    search_fields = ['id', 'name', 'unit', 'quantity', 'price', "total_price", "tax", "money_tax", "total"]
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        return export(self.model._meta, queryset)

    export_as_csv.short_description = "Export Selected"


class SessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'id_user', 'folder']
    list_filter = ['id', 'id_user', 'folder']
    search_fields = ['id', 'folder']
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        return export(self.model._meta, queryset)

    export_as_csv.short_description = "Export Selected"


class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'id_user', 'url', 'upload', 'name', 'status']
    list_filter = ['id', 'id_user', 'url', 'upload', 'name', 'status']
    search_fields = ['id', 'url', 'name', 'status']
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        return export(self.model._meta, queryset)

    export_as_csv.short_description = "Export Selected"


class InfoImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'id_image', 'label', 'text', 'status']
    list_filter = ['id', 'id_image', 'label', 'text', 'status']
    search_fields = ['id', 'label', 'text', 'status']
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        return export(self.model._meta, queryset)

    export_as_csv.short_description = "Export Selected"


# admin.site.register(Distributor, DistributorAdmin)
# admin.site.register(Product, ProductAdmin)
# # admin.site.register(Session, SessionAdmin)
# admin.site.register(Image, ImageAdmin)
# admin.site.register(InfoImage, InfoImageAdmin)
