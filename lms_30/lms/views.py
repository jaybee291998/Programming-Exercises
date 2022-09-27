from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, get_user_model

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

User = get_user_model()
@login_required
def home_view(request):
	user_info = User.objects.get(email=request.user)
	context = {
		'user_info':user_info,
		'title':'Home',
		'edit_profile_link':'http://'+get_current_site(request).domain + reverse('edit_profile'),
		'my_classes_link':'http://'+get_current_site(request).domain + reverse('myclasses_view'),
		'create_class_link':'http://'+get_current_site(request).domain+reverse('create-class'),
		'logout_link':'http://'+get_current_site(request).domain+reverse('logout')
	}
	return render(request, "home/home.html", context)