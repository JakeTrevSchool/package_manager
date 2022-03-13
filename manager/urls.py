from unicodedata import name
from django.urls import path
from manager import views

app_name = 'manager'


urlpatterns = [
    path('', views.index, name='index'),
    path('packages/', views.packages, name='explore'),
    path('package/', views.package, name='package'),
    path('add_package', views.add_package, name="add_package"),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
]