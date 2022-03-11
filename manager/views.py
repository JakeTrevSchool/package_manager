from django.shortcuts import render
from django.http import HttpResponse
from manager.models import UserProfile, Package
# Create your views here.


def index(request):
    context = {
        'developers': UserProfile.objects.count(),
        'packages': Package.objects.count()
    }
    return render(request, 'home.html', context=context)

def packages(request):
    return render(request, 'packages.html')

def package(request):
    return render(request, 'package.html')

def add_package(request):
    return render(request, 'add_package.html')

def contact(request):
    return render(request, 'contact.html')

def login(request):
    return HttpResponse("this is the login page")