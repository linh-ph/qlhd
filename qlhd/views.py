from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from .forms import DistributorForm


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class ScanInvoice(View):
    @classmethod
    def get(cls, request):
        form = DistributorForm()

        return render(request, 'home/index.html', {'form': form})

    @classmethod
    def post(cls, request):
        form = DistributorForm()
        return render(request, 'home/index.html', {'form': form})
