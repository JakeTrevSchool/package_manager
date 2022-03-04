from unicodedata import name
from django.urls import path
from manager import views

app_name = 'manager'


urlpatterns = [
    path('', views.index, name='index'),
    path('explore/', views.explore, name='explore'),
    path('login/', views.login, name='login'),
]