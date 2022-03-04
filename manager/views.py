from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    context = {'developers':0, 'packages':-1}
    return render(request, 'home.html', context=context)

def explore(request):
    return HttpResponse("this is the explore page")

def login(request):
    return HttpResponse("this is the login page")