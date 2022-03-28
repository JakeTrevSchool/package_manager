from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='avatars', blank=True, null=True, default="")

    def __str__(self):
        return self.user.username


class Package(models.Model):
    package_name = models.CharField(max_length=120, unique=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    tags = models.TextField(blank=True)
    current_version = models.CharField(max_length=20, default="0.0.0")

    def getUploadDir(instance, filename):
        return f"packages/{instance.package_name}/readme.md"

    readme = models.FileField(upload_to=getUploadDir)

    downloads = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    public = models.BooleanField(default=0)

    def __str__(self) -> str:
        return self.package_name


class Version(models.Model):
    def getUploadDir(instance, filename):
        return f"packages/{instance.package.package_name}/{instance.version_ID}/{filename}"

    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    version_ID = models.CharField(max_length=20, unique=True)

    code_file = models.FileField(upload_to=getUploadDir)

    comment = models.TextField(default="", blank=True)
    dependencies = models.TextField(default="", blank=True)

    def __str__(self) -> str:
        return self.package + ":" + self.version_ID

# this was never used, but you can see the intention here
class Comment(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    text = models.TextField()

    posted_at = models.DateField()
    likes = models.IntegerField()

    def __str__(self) -> str:
        return self.text[:10]
