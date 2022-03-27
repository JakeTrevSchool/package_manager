import datetime
from django.contrib.auth.models import User
from django.http import HttpRequest
from manager.models import UserProfile, Package

# helper methods


def getUserPackages(user: User):
    author = UserProfile.objects.get(user=user)
    packages = Package.objects.filter(author=author)
    return packages


def is_owner(package: Package, user: User):
    is_owner = False
    if (user.is_authenticated):
        is_owner = (package.author == UserProfile.objects.get(user=user))
    return is_owner


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def handle_package_view_count_cookies(request: HttpRequest, package: Package):
    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                               str(datetime.now()))

    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        package.views = package.views + 1
        package.save()

        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
