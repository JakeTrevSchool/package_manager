from django.contrib import admin
from manager.models import UserProfile, Package, Version, Comment
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Package)
admin.site.register(Version)
admin.site.register(Comment)
