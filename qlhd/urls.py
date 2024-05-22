from django.urls import path
from .views import ScanInvoice, index

urlpatterns = [
    path("", index, name="index"),
    # path('upload-image', upload_image, name="upload_image"),
    path('page', ScanInvoice.as_view(), name="index"),
]