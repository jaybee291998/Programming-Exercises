from django import template
from django.contrib.sites.shortcuts import get_current_site
register = template.Library()

from django.http import HttpResponse

from lms_admin.models import Admin

@register.simple_tag
def domain(request):
    return 'http://'+get_current_site(request).domain

@register.simple_tag
def is_admin(request):
    if Admin.objects.get(model_name='announcement').admins.all().filter(pk=request.user.id).exists():
    	domain = get_current_site(request).domain
    	return f'http://{domain}/lmsadmin/my-announcements/'
    return '#'