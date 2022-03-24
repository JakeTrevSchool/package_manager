from dataclasses import field
from django import forms
from manager.models import UserProfile, Package, Version, Comment


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar',)

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ('package_name', 'tags', 'public', 'readme')

class VersionForm(forms.ModelForm):
    new_current = forms.BooleanField()
    class Meta:
        model = Version
        fields = ('version_ID', 'dependencies', 'comment', "code_file")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
