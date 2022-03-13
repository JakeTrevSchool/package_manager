from django.shortcuts import render
from django.http import HttpResponse
from manager.models import UserProfile, Package
# Create your views here.


def index(request):
    context = {
        'developers': UserProfile.objects.count(),
        'packages': Package.objects.count()
    }
    return render(request, 'manager/home.html', context=context)

def explore(request):
    return render(request, 'manager/explore.html')

def package(request):
    return render(request, 'manager/package.html')

def add_package(request):
    return render(request, 'manager/add_package.html')

def contact(request):
    return render(request, 'manager/contact.html')

def login(request):
    return HttpResponse("this is the login page")