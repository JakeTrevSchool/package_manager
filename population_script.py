
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'package_manager.settings')

django.setup()

# must go second?
from django.core.files.base import File
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from manager.models import UserProfile, Package, Version

PASSWORDS = ['123456', 'bananasforever',  'dwa902p5',
             'skyrim_King43', 'secure_password', ]

NEW_USER_DATA = [
    {
        'username': 'gamer6',
        'email': "game6@test.com",
    },


    {
        'username': '12CrustyBanana21',
        'email': "12cb21@test.com",
    },

    {
        'username': 'Arctic_Official',

        'email': "arcticOfficial@test.com",
    },

    {
        'username': 'theSimonDragon',

        'email': "simonD@test.com",
    },
    {
        'username': 'default_john',

        'email': "john@test.com",
    },
]

NEW_PACKAGE_DATA = [
    {
        # "author" must be added in script - via random choice
        "package_name": "superGreatPackage",
        "tags": "amazing, wonderful",
        "current_version": "1.0.0",
        # "readme": must be extracted from list
        "downloads": 0,
        "views": 0,
        "public": True,
    },
    {
        "package_name": "second_package",
        "tags": "superb",
        "current_version": "1.0.0",
        "downloads": 0,
        "views": 0,
        "public": True,
    },
    {
        "package_name": "horrible_bad_package",
        "tags": "evil, wretched",
        "current_version": "1.0.0",
        "downloads": 0,
        "views": 0,
        "public": False,
    },
    {
        "package_name": "mediocre_package",
        "tags": "average, uninspired",
        "current_version": "1.0.0",
        "downloads": 0,
        "views": 0,
        "public": True,
    },
    {
        "package_name": "sneakyPackage",
        "tags": "",
        "current_version": "1.0.0",
        "downloads": 0,
        "views": 0,
        "public": False,
    },
]


def create_users():
    print("Creating users")
    new_user_profile: UserProfile
    for i, user_data in enumerate(NEW_USER_DATA):
        new_user: User
        new_user, _created = User.objects.get_or_create(**user_data)
        new_user.password = make_password(PASSWORDS[i])
        new_user.save()

        new_user_profile, _created = UserProfile.objects.get_or_create(
            user=new_user)
        with open("population_data/avatars/chew.jpg", "rb") as f:
            new_user_profile.avatar.save(
                new_user.username + "_avatar.jpg", File(f))
        new_user_profile.save()
    return new_user_profile


def create_packages(author: UserProfile):
    print("creating packages")
    print("author will be ", author.user.username)
    for i, package_data in enumerate(NEW_PACKAGE_DATA):
        package: Package
        package, _created = Package.objects.get_or_create(
            **package_data, author=author)
        with open(f"population_data/package_readmes/{i + 1}.md", "rb") as f:
            package.readme.save(
                f"packages/{package_data['package_name']}/readme.md", File(f))
        package.save()


def create_versions():
    # adds two versions for each package
    print("adding versions")
    for i, each in enumerate(Package.objects.all()):
        i = i*2
        i += 1
        version_data = {
            "package": each,
            "version_ID": f"1.0.{i}",
            "comment": f"a new version! specifically, file #{i}",
            "dependencies": "none,"
        }
        new_version, _created = Version.objects.get_or_create(**version_data)
        with open(f"population_data/code_files/{i}.tsx", "rb") as f:
            new_version.code_file.save(f"code_{i}.tsx", File(f))
        new_version.save()

        # add second version
        i += 1
        version_data = {
            "package": each,
            "version_ID": f"1.0.{i}",
            "comment": f"a new version! specifically, file #{i}",
            "dependencies": "none,"
        }
        new_version, _created = Version.objects.get_or_create(**version_data)
        with open(f"population_data/code_files/{i}.tsx", "rb") as f:
            new_version.code_file.save(f"code_{i}.tsx", File(f))
        new_version.save()

        each.current_version = f"1.0.{i}"
        each.save()

    ...


def populate():
    author = create_users()
    create_packages(author)
    create_versions()


if __name__ == '__main__':  # begin execution
    print('Starting population script...')
    populate()
