from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path('upload-image', upload_image, name="upload_image"),
]