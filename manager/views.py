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

def explore(request):
    return HttpResponse("this is the explore page")

def login(request):
    return HttpResponse("this is the login page")