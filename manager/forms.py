import re
from django import forms
from manager.models import UserProfile, Package, Version, Comment


def contains_space(test: str):
    return bool(re.search("\s", test))


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar',)


class PackageForm(forms.ModelForm):

    def clean_package_name(self):
        package_name = self.data.get('package_name')
        if contains_space(package_name):
            raise forms.ValidationError(
                "Your package name must not include spaces", code='invalid')
        return package_name

    class Meta:
        model = Package
        fields = ('package_name', 'tags', 'public', 'readme')


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ('version_ID', 'dependencies', 'comment', "code_file")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class ReadmeForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ('readme',)
