from unicodedata import name
from django.urls import path
from manager import views

app_name = 'manager'


urlpatterns = [
    path('', views.index, name='index'),
    path('explore/', views.explore, name='explore'),
    path('contact/', views.contact, name='contact'),

    path('explore/<int:page>', views.explore, name='explore'),

    path('add_package', views.add_package, name="add_package"),
    path('package/<slug:package_name>', views.package, name='package'),
    path('package/<slug:package_name>/add_version',
         views.add_version, name="add_version"),
    path('package/<slug:package_name>/<str:version>',
         views.get_code, name="get_code"),
    path('package/<slug:package_name>/<str:version>/get',
         views.download, name="download"),
    path('package/<slug:package_name>/readme',
         views.edit_readme, name="edit_readme"),

    path('profile/<slug:profile_name>', views.profile, name="profile"),
    path('accounts/register_profile',
         views.register_profile, name="register_profile"),
]
