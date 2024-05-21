from django.shortcuts import render
from django.views import View
from .forms import DistributorForm, RegistrationForm
from django.http import HttpResponseRedirect

# Create your views here.
class Index(View):
    def get(self, request):
        form = DistributorForm()

        return render(request, 'home/index.html', {'form': form})

    def post(self, request):
        form = DistributorForm()
        return render(request, 'home/index.html', {'form': form})


# Create your views here.
class Home(View):
    def get(self, request):
        form = DistributorForm()

        return render(request, 'home/home.html', {'form': form})

    def post(self, request):
        form = DistributorForm()
        return render(request, 'home/home.html', {'form': form})

def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/admin')
    return render(request, 'pages/register.html', {'form': form})
