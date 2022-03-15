from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', blank = True, null = True)

    def __str__(self):
        return self.user.username

class Package(models.Model):
    #!is this a good way to do this?
    #!i suppose it indicates "ownership"
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    tags = models.TextField()

    package_name = models.CharField(max_length=120, unique=True)
    current_version = models.TextField() #idk how to sort this one out ngl

    downloads = models.IntegerField()
    views = models.IntegerField()
    public = models.BooleanField()
    #!we could also do this as a json-encoded array. opinions?

class Version(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    version_ID = models.CharField(max_length=20)
    code = models.FileField(upload_to="packages/<package_name>")
    commit = models.TextField()
    dependencies = models.TextField() #!encode as json?

class Comment(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    text = models.TextField()

    posted_at = models.DateField()
    likes = models.IntegerField()