from django.contrib import admin
from qlhd.models import Customer, Product, Orders, Feedback, OrdersDetail


class CustomerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Customer, CustomerAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'unit', 'price', 'description')
    search_fields = ['name', 'price', 'type']
    list_filter = ('name', 'price', 'type')


admin.site.register(Product, ProductAdmin)


class OrderAdmin(admin.ModelAdmin):
    pass


admin.site.register(Orders, OrderAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    pass


admin.site.register(Feedback, FeedbackAdmin)


class OrdersDetailAdmin(admin.ModelAdmin):
    pass


admin.site.register(OrdersDetail, OrdersDetailAdmin)
