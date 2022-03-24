import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','package_manager.settings')

## NOTE: Create user profiles too

import django
django.setup() #always do this first


from django.contrib.auth.models import User
from manager.models import UserProfile, Package, File, Version

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

    for i in range(user_profiles.length()):
        new_user = User.objects.create(
            username = i['username'],
            first_name = i['first_name'],
            last_name = i['last_name'],
            password = i['password'],
        )
        new_user.save()
    

def populate():
    #1. create lists of dictionaries containing pages we want to add into each category
    #2. create a dictionary of dictionaries for our categories
    # - allows us to iterate through each data structure, and add the data to our models.

    packages = [ ##placeholder names
        {'author': 'newacc0121c4',
         'tags': 'test',
         'package_name': 'TestProject',
         'current_version': '1.0',
         'downloads': 3,
         'views': 7,
         'public': False},

        {'author': 'notches_biggestfan',
         'tags': 'minecraft, dependancy',
         'package_name': 'tekkit_mekdependancy_121c',
         'current_version': '12.1C',
         'downloads': 12051,
         'views': 125709,
         'public': True},

        {'author': 'newacc0121c4',
         'tags': 'bugfix, patch, vegas',
         'package_name': 'vegas_extension_patch_v6',
         'current_version': '6',
         'downloads': 5002,
         'views': 8091,
         'public': True}]



    #Creating these categories based off of the design spec
    #However, I'm unsure if this is the correct approach.
    #Will the website scripts sort 'most views' and 'user' itself?
    #In that case, these categories could all use the same package pages
    cats = [
        {"name": 'Explore Packages',
        "pages": packages,},

        {"name": 'User Packages',
        "pages": packages,},

        {"name": 'Most Viewed Packages',
        "pages": packages,}]


    #not done
    for cat in cats:          #goes through cats dict
        c = add_cat(cat['name'], cat['pages'])
        for p in cat['pages']:     
            add_page(c, p['name'], p['version'], p['downloads'], p['views'], p['public'], p['tags'])
            #adds associated pages for that category

    for c in Category.objects.all():            #prints categories added
        for p in Page.objects.filter(category = c):
            print(f'- {c}: {p}')


def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p


def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.likes = likes
    c.views = views
    c.save()
    return c

if __name__ == '__main__':                      #begin execution
    print('Starting Rango population script...')
    populate()
            
