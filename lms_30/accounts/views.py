from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm, EditProfileForm, ResendVerificationForm
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.views import View
# Create your views here.

#stuffs needed for email
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

#for random number generation
import random
from django.contrib.auth import get_user_model
User = get_user_model()

#for token
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from .utils import token_generator
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from accounts.models import Profile

# for API
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http import JsonResponse

from .serializers import LogInSerializer

# send email asynch
from lms.task import send_email_task

# login using an api
@api_view(['POST'])
def login_api_view(request):
	if request.method == 'POST':
		serializer = LogInSerializer(data=request.data)
		if serializer.is_valid():
			email = serializer.data['email']
			password = serializer.data['password']
			print('email: ', email)
			print('password: ', password)
			user = authenticate(email=email, password=password)
			if user is not None:
				login(request, user)
				print('Authenticated User: ', request.user)
				return Response(serializer.data['email'])
			
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def login_view(request):
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		email = form.cleaned_data.get('email')
		password = form.cleaned_data.get('password')
		user = authenticate(email=email, password=password)
		login(request, user)
		# print(user)
		if request.user.profile.get_fullname() == ' ':
			return redirect('edit_profile')
		return redirect("home")
	context = {
		'form': form,
		'title': "Login Page",
		'register_link':'http://'+get_current_site(request).domain+reverse('register'),
		'resend_verification_link':'http://'+get_current_site(request).domain + reverse('resend-verification-link')
		}
	
	return render(request, 'accounts/login.html', context)	


def register_view(request):
	next = request.GET.get('next')
	form = UserRegisterForm(request.POST or None)
	messages = []
	errors = []
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.is_active = False

		user.save()
		
		new_user = authenticate(email=user.email, password=password)

		#links
		uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
		domain = get_current_site(request).domain
		link = reverse('verification', kwargs={'uidb64':uidb64, 'token':token_generator.make_token(user)})
		activate_url = "http://" + domain + link
		# Sends the confirmation email
		subject = "Activate your account"
		body = "Hi " + user.email + " please use this link to activate your account.\n" + activate_url
		send_email_task.delay(subject, body, [user.email])
		messages.append('An confirmation email containing a verification link has been sent to the email address that you provided. Please check your spam box, then mark the email not as spam.')
		context = {
			'messages':messages,
			'errors':errors,
			'go_back_link':'http://'+get_current_site(request).domain + reverse('login')
		}
		return render(request, 'learner_management/confirmation.html', context)
	context = {
		'form':form,
		'title':"Sign-up Page",
		'login_link':'http://'+get_current_site(request).domain+reverse('login'),
		'password_reset_link':'http://'+get_current_site(request).domain+reverse('password_reset')
		}
	return render(request, 'accounts/signup.html', context)	

@login_required
def edit_profile_view(request):
	form = EditProfileForm(instance = request.user.profile)

	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
		if form.is_valid():
			form.save()
	profile_pic = request.user.profile.profile_pic.url
	context = {
		'form' : form,
	 	'title':'Edit Profile', 
	 	'profile_pic':profile_pic, 
	 	'profile_empty':request.user.profile.get_fullname()==' ',
	 	'is_instructor':request.user.profile.is_instructor,
	 	'request_instructorship_link':'http://'+get_current_site(request).domain+reverse('request-instructorship')
	 	}
	return render(request, 'accounts/editprofile.html', context)



def verification_view(request, uidb64, token, *args, **kwargs):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	confirmation_success = False
	if user is not None and token_generator.check_token(user, token):
		user.is_active = True
		user.is_confirmed = True
		user.save()
		profile = Profile(user=user)
		profile.save()
		login(request, user)
		messages.success(request, ('Your account has been confirmed.'))
		confirmation_success = True
		return redirect('edit_profile')
	else:
		messages.warning(request, ('The confirmation link is invalid, possibly because it has already been used.'))
		return redirect('register')

	# context = {
	# 	'login_link':'http://'+get_current_site(request).domain+reverse('login'),
	# 	'confirmation_sucess':confirmation_success

	# }
	# return render(request, 'accounts/signup_confirmation.html', context)

def logout_view(request):
	logout(request)
	return redirect('login')

# resend the confirmation link
def resend_verification_link(request):
	form = ResendVerificationForm()
	messages = []
	errors = []
	if request.method == 'POST':
		form = ResendVerificationForm(request.POST)
		if form.is_valid():
			user = User.objects.get(email=form.cleaned_data.get('email'))
			# check if the user is not yet active
			if not user.is_active:
				# send the verification link
				uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
				domain = get_current_site(request).domain
				link = reverse('verification', kwargs={'uidb64':uidb64, 'token':token_generator.make_token(user)})
				activate_url = "http://" + domain + link
				# Sends the confirmation email
				subject = "Activate your account"
				body = "Hi " + user.email + " please use this link to activate your account.\n" + activate_url
				send_email_task.delay(subject, body, [user.email])
				messages.append('An confirmation email containing a verification link has been sent to the email address that you provided. Please check your spam box, then mark the email not as spam.')
			else:
				errors.append('You are already verified, there is no longer a need to resend the verification link')
			context = {
				'messages':messages,
				'errors':errors,
				'go_back_link':'http://'+get_current_site(request).domain + reverse('login')
			}
			return render(request, 'learner_management/confirmation.html', context)
	context = {
		'form':form
	}

	return render(request, 'accounts/resend_verification_link.html', context)



