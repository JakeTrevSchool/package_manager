from unicodedata import name
from django.urls import path
from manager import views

app_name = 'manager'


urlpatterns = [
    path('', views.index, name='index'),
    path('explore/', views.explore, name='explore'),
    path('package/', views.package, name='package'),
    path('add_package', views.add_package, name="add_package"),
    path('contact/', views.contact, name='contact'),
    path('accounts/register_profile', views.register_profile, name="register_profile")
]