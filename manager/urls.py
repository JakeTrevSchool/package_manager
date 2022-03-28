from unicodedata import name
from django.urls import path, re_path
from manager import views

app_name = 'manager'


urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),

    path('explore/', views.explore, name='explore'),
    path('explore/<int:page>/', views.explore, name='explore'),

    path('search/', views.search_packages, name='search_packages'),
    path('search/<str:query>/', views.search_packages, name='search_packages'),
    path('search/<str:query>/<int:page>/',
         views.search_packages, name='search_packages'),

    path('add_package', views.add_package, name="add_package"),

    path('package/<slug:package_name>/', views.package, name='package'),
    path('package/<slug:package_name>/delete/',
         views.delete_package, name='delete_package'),
    path('package/<slug:package_name>/add_version/',
         views.add_version, name="add_version"),
    path('package/<slug:package_name>/get/<str:version>/',
         views.get_package_code, name="get_code"),

    path('package/update_download/<slug:package_name>/',
         views.update_download_count, name="update_downloads"),
    path('package/<slug:package_name>/readme/',
         views.edit_package_readme, name="edit_readme"),

    path('profile/<slug:profile_name>/', views.profile, name="profile"),
    path('profile/<slug:profile_name>/<int:page>',
         views.profile, name="profile"),

    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('accounts/register_profile/',
         views.register_profile, name="register_profile"),
]
