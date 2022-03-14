from django import template
from manager.models import UserProfile

register = template.Library()

@register.inclusion_tag('manager/UserProfile.html')
def get_profile_picture():
	return UserProfile.objects.get.all()