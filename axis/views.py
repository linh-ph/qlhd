from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views import View
from axis.forms import StoreForm
from api.models import Image


# Create your views here.
class Axis(View):
    def post(self, request):
        return render(request, 'axis/index.html', {})

    def get(self, request, id):
        return render(request, 'axis/index.html', {"id": id})


class List(View):
    def get(self, request):
        # form = StoreForm()
        # store = Image.objects.all()
        form = None
        store = None
        return render(request, 'list/index.html', {"form": form, "store": store})

    def post(self, request):
        form = StoreForm()
        return render(request, 'list/index.html', {"form": form})
