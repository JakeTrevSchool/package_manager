
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','package_manager.settings')

## NOTE: Create user profiles too

import django
import datetime
django.setup() #always do this first


from django.contrib.auth.models import User
from manager.models import UserProfile, Package, File, Version, Comment

created_users = []

def create_users():
    ##ideally I would generate x amount of users but
    ##tricky to implement meaningful and realistic data this way

    user_profiles = [
        {'username': 'gamer6',
         'first_name': 'John',
         'last_name': 'Onions',
         'password': '123456',},

        {'username': '12CrustyBanana21',
         'first_name': 'Pedro',
         'last_name': 'Gold',
         'password': 'bananasforever'},

        {'username': 'Arctic_Official',
         'first_name': '',
         'last_name': '',
         'password': 'dwa902p5'},

        {'username': 'theSimonDragon',
         'first_name': 'Simon',
         'last_name': 'Dragon',
         'password': 'skyrim_King43'}
        ]

    print("Creating users")

    for j, i in enumerate(user_profiles):
        new_user = User.objects.create(
            username = i['username'],
            first_name = i['first_name'],
            last_name = i['last_name'],
            password = i['password'],
        )
        created_users[j] = new_user
        new_user.save()
    

def populate():
    #1. create lists of dictionaries containing pages we want to add into each category
    #2. create a dictionary of dictionaries for our categories
    # - allows us to iterate through each data structure, and add the data to our models.

##users
    create_users()
    for i in created_users:
        add_user(i)   

##packages  
    add_package(
        author = UserProfiles.objects.filter(username='theSimonDragon').first(),
        tags = 'test',
        package_name = 'TestProject',
        current_version = '1.0',
        downloads = 3,
        views = 7,
        public = False)

    add_package(
        author = UserProfiles.objects.filter(username='gamer6').first(),
        tags = 'minecraft, dependancy, game, mod',
        package_name = 'tekkit_mekdependancy_121c',
        current_version = '12.1C',
        downloads = 12051,
        views = 50921,
        public = True)

    add_package(
        author = UserProfiles.objects.filter(username='Arctic_Official').first(),
        tags = 'bugfix, patch, vegas, extension',
        package_name = 'vegas_extension_patch_v6',
        current_version = '6a',
        downloads = 849252,
        views = 1000000,
        public = True)

##versions    
    add_version(
        package = Package.objects.filter(package_name="TestProject").first(),
        version_ID = "1.0",
        code_file = v.getUploadDir("test1.txt"),
        comment = "",
        dependencies = "")

    add_version(
        package = Package.objects.filter(package_name="tekkit_mekdependancy_121c").first(),
        version_ID = "12.1C",
        code_file = v.getUploadDir("test2.txt"),
        comment = "Latst patch for tekkit v12",
        dependencies = "Minecraft")

    add_version(
        package = Package.objects.filter(package_name="vegas_extension_patch_v6").first(),
        version_ID = "6a",
        code_file = v.getUploadDir("test3.txt"),
        comment = "Bugfix for sony extension",
        dependencies = "Vegas, ExtensionName1")

##comments
    add_comment(
        author = UserProfiles.objects.filter(username='theSimonDragon').first(),
        package = Package.objects.filter(package_name="tekkit_mekdependancy_121c").first(),
        text = "thanks for fix :)",
        posted_at = datetome.date(2022,3,10),
        likes = 128)

    add_comment(
        author = UserProfiles.objects.filter(username='gamer6').first(),
        package = Package.objects.filter(package_name="tekkit_mekdependancy_121c").first(),
        text = "Took you long enough.",
        posted_at = datetome.date(2022,3,7),
        likes = 2)

    add_comment(
        author = UserProfiles.objects.filter(username='Arctic_Official').first(),
        package = Package.objects.filter(package_name="vegas_extension_patch_v6").first(),
        text = "Let me know of any issues here!",
        posted_at = datetome.date(2021,10,28),
        likes = 52)


def add_user(user, avatar=None):
    u = UserProfile.objects.get_or_create()
    u.user = user
    u.avatar = avatar
    return u

def add_package(author, tags, package_name, current_version, downloads, views, public):
    p = Package.objects.get_or_create()
    p.author = author
    p.tags = tags
    p.package_name = package_name
    p.current_version = version
    p.downloads = downloads
    p.views = views
    p.public = public
    p.save()
    return p

def add_version(package, version_ID, code_file, comment, dependencies):
    v = Version.objects.get_or_create()
    v.package = package
    v.version_ID = version_ID
    v.code_file = v.getUploadDir
    v.comment = comment
    v.dependencies = dependencies

    return v

def add_comment(author, package, text, posted_at, likes):
    c = Comment.objects.get_or_create()
    c.author = author
    c.package = package
    c.text = text
    c.posted_at = posted_at
    c.likes = likes

    return c


if __name__ == '__main__':                      #begin execution
    print('Starting population script...')
    populate()
            
