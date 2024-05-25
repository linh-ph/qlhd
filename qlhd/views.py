from django.http import HttpResponse


def index(request):
    return HttpResponse("APP QLHD index.")
