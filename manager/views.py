from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from manager.forms import UserProfileForm, PackageForm, VersionForm, CommentForm
from manager.models import UserProfile, Package
# Create your views here.

# a helper method
def getUserPackages(user: User):
    author = UserProfile.objects.get(user=user)
    packages = Package.objects.filter(author=author)
    return packages

def index(request):
    context = {
        'developers': UserProfile.objects.count(),
        'packages': Package.objects.count()
    }
    return render(request, 'manager/home.html', context=context)

def contact(request):
    return render(request, 'manager/contact.html')

def explore(request):
    top_packages = Package.objects.filter(public=True)[:5]
    user_packages = getUserPackages(request.user)

    context_dict = {
        'top_packages':top_packages,
        'user_packages':user_packages,
    }
    return render(request, 'manager/explore.html', context=context_dict)

def package(request, package_name):
    package = get_object_or_404(Package, package_name=package_name)
    context_dict = {'package':package}
    return render(request, 'manager/package.html', context=context_dict)

@login_required
def add_package(request):
    form = PackageForm()

    if request.method == 'POST':
        form = PackageForm(request.POST)

        if form.is_valid():
            package = form.save(commit=False)
            package.author = UserProfile.objects.get(user=request.user)

            package.downloads = 0
            package.views = 0
            package.current_version = "0.0.0"
            package.save()
            return redirect('manager:index')
        else:
            print(form.errors)

    return render(request, 'manager/add_package.html', {'form':form})

@login_required
def add_version(request, package_name):
    try:
        package = Package.objects.get(package_name=package_name)
        
        form = VersionForm()

        if request.method == 'POST':
            form = VersionForm(request.POST)

            if form.is_valid():
                version = form.save(commit=False)
                version.package = package
                version.save()

                return redirect('manager:index')
            else:
                print(form.errors)

    except Package.DoesNotExist:
        return HttpResponse("does not exist")



    form = VersionForm()

    if request.method == 'POST':
        form = VersionForm(request.POST)
        if form.is_valid():
            version = form.save(commit=False)

        ...
    return render(request, 'manager/add_version.html', {'form':form})

@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect(reverse('manager:index'))
        else:
            print(form.errors)
    
    context_dict = {'form': form}
    return render(request, 'registration/register_profile.html', context_dict)
    