from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', home_view, name=''),
    path('afterlogin', afterlogin_view, name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='ecom/logout.html'), name='logout'),

    path('search', search_view, name='search'),

    path('adminclick', adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='ecom/adminlogin.html'), name='adminlogin'),
    path('admin-dashboard', admin_dashboard_view, name='admin-dashboard'),

    path('view-customer', view_customer_view, name='view-customer'),
    path('delete-customer/<int:pk>', delete_customer_view, name='delete-customer'),
    path('update-customer/<int:pk>', update_customer_view, name='update-customer'),

    path('admin-products', admin_products_view, name='admin-products'),
    path('admin-add-product', admin_add_product_view, name='admin-add-product'),
    path('delete-product/<int:pk>', delete_product_view, name='delete-product'),
    path('update-product/<int:pk>', update_product_view, name='update-product'),

    path('admin-add-invoice', admin_add_invoice_view, name='admin-add-invoice'),
    path('admin-invoices', admin_invoices_view, name='admin-invoices'),
    path('delete-invoice/<int:pk>', delete_invoice, name='delete-invoice'),
    path('detail-invoice/<int:pk>', update_invoice_view, name='detail-invoice'),

    path('admin-view-booking', admin_view_booking_view, name='admin-view-booking'),
    path('delete-order/<int:pk>', delete_order_view, name='delete-order'),
    path('update-order/<int:pk>', update_order_view, name='update-order'),

    path('customersignup', customer_signup_view),
    path('customerlogin', LoginView.as_view(template_name='ecom/customerlogin.html'), name='customerlogin'),
    path('customer-home', customer_home_view, name='customer-home'),
    path('my-order', my_order_view, name='my-order'),
    path('my-profile', my_profile_view, name='my-profile'),
    path('edit-profile', edit_profile_view, name='edit-profile'),

    path('add-to-cart/<int:pk>', add_to_cart_view, name='add-to-cart'),
    path('cart', cart_view, name='cart'),
    path('remove-from-cart/<int:pk>', remove_from_cart_view, name='remove-from-cart'),
    path('customer-address', customer_address_view, name='customer-address'),
    path('payment-success', payment_success_view, name='payment-success'),
    path('download-order/<int:orderID>/<int:productID>', download_order_view, name='download-order'),
    path('scan-image/', scan_image_view, name='scan_image'),
]
