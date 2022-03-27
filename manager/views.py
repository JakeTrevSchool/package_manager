from django.db.models import Q
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from manager.forms import ReadmeForm, UserProfileForm, PackageForm, VersionForm, CommentForm
from manager.models import UserProfile, Package, Version
from manager.helperMethods import getUserPackages, handle_package_view_count_cookies, is_owner

# Create your views here.
PAGE_SIZE = 5


def index(request: HttpRequest):
    context = {
        'developers': UserProfile.objects.count(),
        'packages': Package.objects.count(),
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

    start_index = (page - 1) * PAGE_SIZE
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
        pages = [page, page + 1, page + 2][:num_pages]
    else:
        pages = [page - 1, page, page + 1][:num_pages]

    context_dict = {
        'packages': top_packages,
        'user_packages': user_packages,
        'packages_before': packages_before,
        'packages_after': packages_after,
        'page': page,
        'pages': pages,
    }
    return render(request, 'manager/explore.html', context=context_dict)


def search_packages(request):
    context = {}
    if request.method == 'GET':
        query = request.GET.get('q')

        if query:
            lookups = Q(package_name__icontains=query) | Q(
                tags__icontains=query)

            results = Package.objects.filter(lookups).distinct()

            context = {'results': results}

    context = {
        'packages': top_packages,
        'packages_before': packages_before,
        'packages_after': packages_after,
        'page': page,
        'pages': pages,
    }
    return render(request, 'manager/explore.html', context=context)


def package(request: HttpRequest, package_name: str):
    package = get_object_or_404(Package, package_name=package_name)

    readme_file = package.readme
    readme = ""
    if readme_file:
        with readme_file.open('r') as f:
            readme = f.read()
    else:
        readme = "# This package does not have a readme"

    # get comments
    comments = []

    # check if user has admin priveliges
    # this could be modified in the future to allow for collaborators
    user_is_owner = is_owner(package, request.user)

    handle_package_view_count_cookies(request, package)

    package_versions = Version.objects.filter(package=package)
    num_versions = package_versions.count()

    try:
        cur_version: Version = Version.objects.get(
            version_ID=package.current_version)
    except Version.DoesNotExist:
        cur_version = None

    versions = [version.version_ID for version in package_versions.all()]

    context_dict = {
        'package': package,
        'user_is_owner': user_is_owner,
        'readme': readme,
        'version_count': num_versions,
        'versions': versions,
    }
    return render(request, 'manager/package.html', context=context_dict)


def get_package_code(request: HttpRequest, package_name: str, version: str):
    package: Package = get_object_or_404(Package, package_name=package_name)
    try:
        requested_version: Version = Version.objects.filter(
            package=package).get(version_ID=version)
        with requested_version.code_file.open('r') as f:
            code_content = f.read()
        url = requested_version.code_file.url
        status = "OK"

    except Version.DoesNotExist:
        code_content = """<h1> Something went wrong! </h1>
        The version you are looking for does not exist."""
        url = ""
        status = "ERROR"

    data = {
        'version': version,
        'status': status,
        'download_url': url,
        'content': code_content,
    }

    return JsonResponse(data)


def update_download_count(request: HttpRequest, package_name: str):
    package: Package = get_object_or_404(Package, package_name=package_name)
    package.downloads += 1
    package.save()
    return HttpResponse()


def edit_package_readme(request: HttpRequest, package_name: str):
    package: Package = get_object_or_404(Package, package_name=package_name)

    if not is_owner(package, request.user):
        return redirect(reverse('manager:package', package_name))

    if request.method == 'POST':
        form = ReadmeForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            form.save()
            return redirect(reverse('manager:index'))
        else:
            print(form.errors)

    form = ReadmeForm(instance=package)
    action = request.get_full_path()

    return render(request, 'manager/form.html', {'form': form, 'action': action})


@login_required
def add_package(request: HttpRequest):
    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES)
        if form.is_valid():
            package = form.save(commit=False)
            package.author = UserProfile.objects.get(user=request.user)

            package.save()
            return redirect('manager:index')
        else:
            print(form.errors)

    form = PackageForm()
    action = request.get_full_path()

    return render(request, 'manager/form.html', {'form': form, 'action': action})


@login_required
def add_version(request: HttpRequest, package_name: str):
    package = get_object_or_404(Package, package_name=package_name)

    if not is_owner(package, request.user):
        return redirect(reverse('manager:package', package_name))

    if request.method == 'POST':
        form = VersionForm(request.POST, request.FILES)
        if form.is_valid():
            version: Version = form.save(commit=False)
            # add package to version.
            version.package = package
            version.save()
            package.current_version = version.version_ID
            package.save()
            return redirect('manager:index')
        else:
            print(form.errors)

    form = VersionForm()
    action = request.get_full_path()

    context_dict = {
        'form': form,
        'action': action,
        'package': package
    }
    return render(request, 'manager/form.html', context_dict)

# move this into user_form


@login_required
def register_profile(request: HttpRequest):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect(reverse('manager:index'))
        else:
            print(form.errors)

    form = UserProfileForm()
    return render(request, 'registration/register_profile.html', {'form': form})


def profile(request: HttpRequest, profile_name: str):
    user = get_object_or_404(User, username=profile_name)
    profile = get_object_or_404(UserProfile, user=user)

    user_packages = getUserPackages(user)[:PAGE_SIZE]

    context_dict = {'profile': profile, 'user_packages': user_packages}
    return render(request, 'manager/profile.html', context=context_dict)


def custom_page_not_found_view(request, exception):
    response = render(request, 'manager/404.html', {})
    response.status_code = 404
    return response
