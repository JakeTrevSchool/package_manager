from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.db.models import QuerySet
from manager.models import UserProfile, Package

# helper methods

PAGE_SIZE = settings.MANAGER_PAGE_SIZE


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


class outOfPagesException(Exception):
    def __init__(self, num_pages, message="tried to get a page out of bounds"):
        self.num_pages = num_pages
        self.message = message
        super().__init__(self.message)


def paginate(data: QuerySet, page: int):
    if not data:
        return data, {
            "num_pages": 1,
            "pages": [1],
            "pages_before": False,
            "pages_after": False
        }

    start_index = (page - 1) * PAGE_SIZE
    end_index = page * PAGE_SIZE

    num_packages = data.count()
    num_pages = ((num_packages - 1) // PAGE_SIZE) + 1

    if page > num_pages:
        raise outOfPagesException(num_pages)

    if page == 1:
        pages = [page, page + 1, page + 2][:num_pages]
    else:
        pages = [page - 1, page, page + 1][:num_pages]

    pages_before = page != 1
    pages_after = page != num_pages

    page_info = {
        "num_pages": num_pages,
        "pages": pages,
        "pages_before": pages_before,
        "pages_after": pages_after
    }

    return data[start_index:end_index], page_info
