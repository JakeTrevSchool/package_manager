import re
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from manager.forms import UserProfileForm, PackageForm, VersionForm, CommentForm
from manager.models import UserProfile, Package, Version
# Create your views here.
PAGE_SIZE = 5



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

    
    # get user packages
    user_packages = []
    if (request.user.is_authenticated):
        user_packages = getUserPackages(request.user)[:PAGE_SIZE]

    start_index = (page-1) * PAGE_SIZE
    end_index = page * PAGE_SIZE

    num_packages = Package.objects.filter(public=True).count()
    num_pages = (num_packages // PAGE_SIZE) + 1
    
    if start_index > num_packages:
        return redirect('manager:explore', num_pages)

    packages_before = page != 1
    packages_after = page != num_pages

    top_packages = Package.objects.order_by('-views')
    top_packages = top_packages.filter(public=True)[start_index:end_index]

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

    # check if user has admin priveliges
    # this could be modified in the future to allow for collaborators.
    user_is_owner = False
    if(request.user.is_authenticated):
        print(package.author)
        print(UserProfile.objects.get(user=request.user))
        user_is_owner = (package.author == UserProfile.objects.get(user=request.user))

    # get comments
    comments = [] 

    context_dict = {'package':package, 'user_is_owner':user_is_owner}
    return render(request, 'manager/package.html', context=context_dict)


@login_required
def add_package(request: HttpRequest):
    form = PackageForm()

    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES)
        if form.is_valid():
            package = form.save(commit=False)
            package.author = UserProfile.objects.get(user=request.user)

            package.save()
            return redirect('manager:index')
        else:
            return redirect('manager:explore')
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

    if request.method == 'POST':
        form = VersionForm(request.POST, request.FILES)
        if form.is_valid():
            version: Version = form.save(commit=False)
            # add package to version.
            version.package = package
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

    user_packages = getUserPackages(user)[:PAGE_SIZE]

    context_dict= {'profile':profile, 'user_packages':user_packages}
    return render(request, 'manager/profile.html', context=context_dict)

def custom_page_not_found_view(request, exception):
    response = render(request, 'manager/404.html', {})
    response.status_code = 404
    return response


