from django.shortcuts import redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from manager.forms import UserProfileForm
from manager.models import UserProfile, Package
# Create your views here.


def index(request):
    context = {
        'developers': UserProfile.objects.count(),
        'packages': Package.objects.count()
    }
    return render(request, 'manager/home.html', context=context)

def explore(request):
    return render(request, 'manager/explore.html')

def package(request):
    return render(request, 'manager/package.html')

def add_package(request):
    return render(request, 'manager/add_package.html')

def contact(request):
    return render(request, 'manager/contact.html')

@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect(reverse('manager:index'))
        else:
            print(form.errors)
    
    context_dict = {'form': form}
    return render(request, 'registration/register_profile.html', context_dict)
    