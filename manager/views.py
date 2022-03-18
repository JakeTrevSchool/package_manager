from mmap import PAGESIZE
from tkinter import Pack
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from manager.forms import UserProfileForm, PackageForm, VersionForm, CommentForm
from manager.models import UserProfile, Package, Version, File
# Create your views here.

# a helper method
def getUserPackages(user: User):
    author = UserProfile.objects.get(user=user)
    packages = Package.objects.filter(author=author)
    return packages

def index(request: HttpRequest):
    context = {
        'developers': UserProfile.objects.count(),
        'packages': Package.objects.count()
    }
    return render(request, 'manager/home.html', context=context)

def contact(request: HttpRequest):
    return render(request, 'manager/contact.html')

def explore(request: HttpRequest, page=1):
    page = int(page)

    PAGE_SIZE = 1
    
    start_index = (page-1) * PAGE_SIZE
    end_index = page * PAGE_SIZE

    num_packages = Package.objects.filter(public=True).count()
    
    num_pages = (num_packages // PAGE_SIZE) + 1
    
    if start_index > num_packages:
        return redirect('manager:explore', num_pages)

    packages_before = page != 1
    packages_after = page != num_pages

    top_packages = Package.objects.filter(public=True)[start_index:end_index]
    user_packages = getUserPackages(request.user)[:10]

    if page == 1:
        pages = [page, page+1, page +2][:num_pages]
    else :
        pages = [page-1, page, page +1][:num_pages]

    context_dict = {
        'top_packages':top_packages,
        'user_packages':user_packages,
        'packages_before': packages_before,
        'packages_after': packages_after,
        'page':page,
        'pages':pages,
    }
    return render(request, 'manager/explore.html', context=context_dict)

def package(request: HttpRequest, package_name: str):
    package = get_object_or_404(Package, package_name=package_name)
    context_dict = {'package':package}
    return render(request, 'manager/package.html', context=context_dict)


@login_required
def add_package(request: HttpRequest):
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


def handle_file_upload(f, destination: str):
    with open(destination, "wb+") as target:
        for chunk in f.chunks():
            target.write(chunk)
    
@login_required
def add_version(request: HttpRequest, package_name:str):
    package = get_object_or_404(Package, package_name=package_name)
    form = VersionForm()

    print("the view is working")
    if request.method == 'POST':
        print("post")
        form = VersionForm(request.POST, request.FILES)
        if form.is_valid():
            print("form validated")
            version: Version = form.save(commit=False)
            version.package = package

            code_files = request.FILES.values()
            
            # compute the destination
            version_id = version.version_ID
            dest = f"packages/{package_name}/{version_id}/"

            for f in code_files:
                handle_file_upload(f, dest + f.name)
                new_f = File(file=f).save()
                version.code_files.add(new_f)
                
            version.save()
            return redirect('manager:index')
        else:
            print (form.errors)

    return render(request, 'manager/add_version.html', {'form':form, 'package':package})

@login_required
def register_profile(request: HttpRequest):
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

def profile(request, profile_name:str):
    user = get_object_or_404(User, username=profile_name)
    profile = get_object_or_404(UserProfile, user=user)

    user_packages = getUserPackages(user)

    context_dict= {'profile':profile, 'user_packages':user_packages}
    return render(request, 'manager/profile.html', context=context_dict)
