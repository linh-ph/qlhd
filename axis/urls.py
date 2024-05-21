from django.urls import path
from .views import Axis, List

urlpatterns = [
    path('detail/<int:id>', Axis.as_view(), name="detail"),
    path('list', List.as_view(), name="list"),
]
