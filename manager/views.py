from django.conf import settings
from django.db.models import Q
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from manager.forms import ReadmeForm, UserProfileForm, PackageForm, VersionForm, CommentForm
from manager.models import UserProfile, Package, Version
from manager.helperMethods import getUserPackages, handle_package_view_count_cookies, is_owner, outOfPagesException, paginate

# Create your views here.
PAGE_SIZE = settings.MANAGER_PAGE_SIZE


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

    top_packages = Package.objects.order_by('-views').filter(public=True)

    try:
        top_packages, context_dict = paginate(top_packages, page)
    except outOfPagesException as e:
        return redirect('manager:explore', e.num_pages)

    context_dict.update({
        'page': page,
        'user_packages': user_packages,
        'packages': top_packages,
        'pagination_url': reverse('manager:explore'),
        'list_null_message': "No packages have been added yet..."
    })
    return render(request, 'manager/explore.html', context=context_dict)


def search_packages(request: HttpRequest, query="", page=1):
    page = int(page)
    results = []

    context_dict = {
        "num_pages": 1,
        "pages": 1,
        "pages_before": False,
        "pages_after": False
    }

    print("page " + str(page))
    print("query " + query)

    if request.method == 'GET':
        if query:
            lookups = Q(package_name__icontains=query) | Q(
                tags__icontains=query)

            results = Package.objects.filter(lookups).distinct()

    if results:
        try:
            results, context_dict = paginate(results, page)
        except outOfPagesException as e:
            return redirect('manager:search_packages', str(query),   e.num_pages)

    context_dict.update({
        'query': query,
        'page': page,
        'packages': results,
        'pagination_url': reverse('manager:search_packages', kwargs={"query": query}),
        'list_null_message': "We can't find any matching packages"
    })
    return render(request, 'manager/explore.html', context=context_dict)


def package(request: HttpRequest, package_name: str):
    package = get_object_or_404(Package, package_name=package_name)

    readme_file = package.readme
    readme = ""
    if readme_file:
        with readme_file.open('r') as f:
            readme = f.read()
    else:
        readme = "# This package does not have a readme"

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


def profile(request: HttpRequest, profile_name: str, page=1):
    user = get_object_or_404(User, username=profile_name)
    profile = get_object_or_404(UserProfile, user=user)

    page = int(page)
    try:
        user_packages, context_dict = paginate(getUserPackages(user), page)
    except outOfPagesException as e:
        return redirect('manager:profile', profile_name, e.num_pages)

    context_dict.update({
        'profile': profile,
        'packages': user_packages,
        'pagination_url':  reverse('manager:profile', kwargs={"profile_name": profile_name}),
        'page': page,
        'list_null_message': "You havent added any packages yet"
    })
    return render(request, 'manager/profile.html', context=context_dict)


def custom_page_not_found_view(request, exception):
    response = render(request, 'manager/404.html', {})
    response.status_code = 404
    return response
