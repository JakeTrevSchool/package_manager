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
        fields = ('package_name', 'tags', 'public')

class VersionForm(forms.ModelForm):
    new_current = forms.BooleanField()
    code = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Version
        fields = ('version_ID', 'dependencies', 'comment')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
