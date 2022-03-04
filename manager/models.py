from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', blank = True)

    def __str__(self):
        return self.user.username

class package(models.Model):
    #!is this a good way to do this?
    #!i suppose it indicates "ownership"
    author = models.ForeignKey(UserProfile)
    collaborators = models.ManyToManyField(UserProfile)

    package_name = models.CharField(max_length=120, unique=True)
    current_version = models.AutoField() #idk how to sort this one out ngl

    downloads = models.IntegerField()
    views = models.IntegerField()
    public = models.BooleanField()
    tags = models.TextField()
    #!we could also do this as a json-encoded array. opinions?

class version(models.Model):
    package = models.ForeignKey(package)
    version_ID = models.CharField(max_length=20)
    code = models.FileField(upload_to="packages/<package_name>")
    dependencies = models.foreignKey()#!this is annother one im not clear on- this doesnt feel like the way

class comment(models.Model):
    author = models.ForeignKey(UserProfile)
    package = models.ForeignKey(package)
    text = models.TextField()