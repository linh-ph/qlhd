from django.http import HttpResponse
from django.urls import path

from .api.scan_image import upload_image, detected_ocr_upload_image
from .views import index

urlpatterns = [
    path("", index, name="index"),
    path('test', lambda request: HttpResponse("This is a test message."), name="test"),

    #
    path('upload-image', upload_image, name="upload_image"),
    path('detected-image', detected_ocr_upload_image, name="detected_ocr_upload_web")
]
