from registration.backends.simple.views import RegistrationView
from django.contrib import admin
from django.urls import path, include
from django.urls import reverse
from django.conf.urls.static import static
from django.conf import settings

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

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'manager.views.custom_page_not_found_view'