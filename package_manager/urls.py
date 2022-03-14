from registration.backends.simple.views import RegistrationView
from django.contrib import admin
from django.urls import path, include
from django.urls import reverse

print(RegistrationView)

class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return reverse('manager:register_profile')

urlpatterns = [
    path('', include('manager.urls')),
    path('admin/', admin.site.urls),
    path('accounts/register/', MyRegistrationView.as_view(), name='registration_register'),
    path('accounts/', include('registration.backends.simple.urls')),
]
