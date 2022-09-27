from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from .forms import AnnouncementForm, AnnouncementImageForm, EditAnnouncementForm
from django.contrib.auth import get_user_model


from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings

# for pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# the user model
User = get_user_model()
from .models import Announcement, AnnouncementImage, Admin


# send asynch email
from lms.task import send_email_task

@login_required
def add_new_announcement_view(request):
	form = AnnouncementForm()
	errors = []
	sucess = []
	# check if the user is in the admin list
	if Admin.objects.get(model_name='announcement').admins.all().filter(pk=request.user.id).exists():
		if request.method == 'POST':
			form = AnnouncementForm(request.POST)
			if form.is_valid():
				a = form.save(commit=False)
				a.author = request.user
				a.save()
				# send a notification email to all lms user
				email_subject = 'New Announcement'
				title = a.title
				description = a.description
				body = f'Title: {title}\nDescription: {description}'
				all_emails_list = [user.email for user in User.objects.all()]
				# the chunk size
				n = settings.CHUNK_SIZE
				chunked_emails_list = [all_emails_list[i:i+n] for i in range(0, len(all_emails_list), n)]
				# send the notification email by chunk
				for emails_chunk in chunked_emails_list:
					send_email_task.delay(email_subject, body, emails_chunk)
				# sucess.append('New Announcement added')
				return redirect('add-announcement-image', announcement_id=urlsafe_base64_encode(force_bytes(a.id)))
			else:
				errors.append('Form invalid')
	else:
		return redirect('home')

	context = {
		'form':form,
		'errors':errors,
		'sucess':sucess
	}
	return render(request, 'lms_admin/add_announcement.html', context)
@login_required
def add_announcement_image_view(request, announcement_id):
	try:
		decoded_announcement_id = force_bytes(urlsafe_base64_decode(announcement_id))
		specific_announcement = Announcement.objects.get(pk=decoded_announcement_id)
	except(TypeError, ValueError, OverflowError, Announcement.DoesNotExist):
		specific_announcement = None
	form = AnnouncementImageForm()
	existing_announcement_images = []
	errors = []
	if specific_announcement is not None:
		existing_images = specific_announcement.announcementimages.all()
		if Admin.objects.get(model_name='announcement').admins.all().filter(pk=request.user.id).exists():
			form = AnnouncementImageForm(request.POST, request.FILES)
			if request.method == 'POST':
				if form.is_valid():
					a = form.save(commit=False)
					a.announcement = specific_announcement
					a.save()
		else:
			return redirect('home')
	else:
		return redirect('home')

	if specific_announcement is not None:
		for existing_image in specific_announcement.announcementimages.all():
			delete_link = 'http://'+get_current_site(request).domain+reverse('delete-announcement-image', kwargs={'announcement_image_id':urlsafe_base64_encode(force_bytes(existing_image.id)), 'announcement_id':announcement_id})
			efi = (existing_image.image.name, existing_image.image.url, delete_link)
			existing_announcement_images.append(efi)

	context = {
		'form':form,
		'title':specific_announcement.title,
		'announcement_images_info':existing_announcement_images,
		'errors':errors,
		'go_back_link':'http://'+get_current_site(request).domain+reverse('specific-announcement', kwargs={'announcement_id':announcement_id})
	}

	return render(request, 'lms_admin/add_announcement_image.html', context)

@login_required
def delete_announcement_image_view(request, announcement_image_id, announcement_id):
	try:
		decoded_announcement_image_id = force_bytes(urlsafe_base64_decode(announcement_image_id))
		specific_announcement_image = AnnouncementImage.objects.get(pk=decoded_announcement_image_id)
	except(AnnouncementImage.DoesNotExist):
		specific_announcement_image = None;

	if specific_announcement_image is not None:
		if Admin.objects.get(model_name='announcement').admins.all().filter(pk=request.user.id).exists():
			specific_announcement_image.delete()
			return redirect('add-announcement-image', announcement_id=announcement_id)
	# return redirect('add-lesson-file', lesson_id = lesson_id)
	return redirect('home')


@login_required
def specific_announcement_view(request, announcement_id):
	try:
		decoded_announcement_id = force_bytes(urlsafe_base64_decode(announcement_id))
		specific_announcement = Announcement.objects.get(pk=decoded_announcement_id)
	except(Announcement.DoesNotExist):
		specific_announcement = None

	announcement_images_info = []
	if specific_announcement is not None:
		if Admin.objects.get(model_name='announcement').admins.all().filter(pk=request.user.id).exists():
			announcement_images = specific_announcement.announcementimages.all() #LessonFile.objects.filter(lesson=specific_lesson)
			# get the name of the file and there link
			for announcement_image in announcement_images:
				lfi = (announcement_image.image.name, announcement_image.image.url)
				announcement_images_info.append(lfi)
			add_announcement_image_link = 'http://'+get_current_site(request).domain + reverse('add-announcement-image', kwargs={'announcement_id':announcement_id})
		else:
			return redirect('home')
	else:
		return redirect('home')

	context = {
		'announcement':specific_announcement,
		'announcement_images_info':announcement_images_info,
		'add_announcement_image_link':add_announcement_image_link,
		'go_back_link': 'http://'+get_current_site(request).domain + reverse('my-announcements'),
		'edit_announcement_link': 'http://'+get_current_site(request).domain + reverse('edit-announcement', kwargs={'announcement_id':announcement_id}),
		'delete_announcement_link': 'http://'+get_current_site(request).domain + reverse('delete-announcement', kwargs={'announcement_id':announcement_id})
	}
	return render(request, 'lms_admin/specific_announcement.html', context)

@login_required
def my_announcements_view(request):
	announcements_info = []
	if Admin.objects.get(model_name='announcement').admins.all().filter(pk=request.user.id).exists():
		domain = 'http://'+get_current_site(request).domain
		# links
		announcements_link = domain+reverse('my-announcements')
		instructors_link = domain+reverse('instructors')
		pending_instructors_link = domain+reverse('pending-instructors')
		all_announcement = Announcement.objects.all()
		for announcement in all_announcement:
			announcement_link = reverse('specific-announcement', kwargs={'announcement_id':urlsafe_base64_encode(force_bytes(announcement.pk))})
			li = (announcement.title, domain+announcement_link, announcement.timestamp, announcement.author.profile.get_fullname(), announcement.author.profile.profile_pic.url, announcement.description)
			announcements_info.append(li)
		announcements_info.sort(key=lambda a:a[2], reverse=True)
	context = {
		'announcements_link':announcements_link,
		'instructors_link':instructors_link,
		'pending_instructors_link':pending_instructors_link,
		'announcements_info':announcements_info,
		'add_announcement_link':domain+reverse('add-new-announcement'),
	}

	return render(request, 'lms_admin/my_announcements.html', context)

@login_required
def instructors_view(request):
	if Admin.objects.get(model_name='announcement').admins.all().filter(pk=request.user.id).exists():
		# get all instructors
		all_instructors = User.objects.filter(profile__is_instructor=True)

		domain = 'http://'+get_current_site(request).domain

		announcements_link = domain+reverse('my-announcements')
		instructors_link = domain+reverse('instructors')
		pending_instructors_link = domain+reverse('pending-instructors')


		instructors_info = []
		for instructor in all_instructors:
			revoke_link = domain+reverse('revoke-instructorship', kwargs={'instructor_id':urlsafe_base64_encode(force_bytes(instructor.pk))})
			instructors_info.append((instructor.profile.profile_pic.url, instructor.profile.get_fullname(), instructor.id, revoke_link))

		instructors_info_page = request.GET.get('ii_page', 1)
		instructors_info_paginator = Paginator(instructors_info, 20)

		try:
			instructors_info_sp = instructors_info_paginator.page(instructors_info_page)
		except PageNotAnInteger:
			instructors_info_sp = instructors_info_paginator.page(1)
		except EmptyPage:
			instructors_info_sp = instructors_info_paginator.page(paginator.num_pages)

		admins_info = []
		for admin in Admin.objects.get(model_name='announcement').admins.all():
			admins_info.append((admin.profile.profile_pic.url, admin.profile.get_fullname(), admin.id))

		context = {
			'announcements_link':announcements_link,
			'instructors_link':instructors_link,
			'pending_instructors_link':pending_instructors_link,
			'instructors_info_sp':instructors_info_sp,
			'admins_info':admins_info,
			'is_admin':Admin.objects.get(model_name='announcement').admins.all().filter(pk=request.user.id).exists()
		}

		return render(request, 'lms_admin/instructors.html', context)

@login_required
def pending_instructors_view(request):
	if Admin.objects.get(model_name='announcement').admins.all().filter(pk=request.user.id).exists():
		# get all pending instructors
		all_pending_instructors = Admin.objects.get(model_name='announcement').pending_instructors.all()

		domain = 'http://'+get_current_site(request).domain

		announcements_link = domain+reverse('my-announcements')
		instructors_link = domain+reverse('instructors')
		pending_instructors_link = domain+reverse('pending-instructors')


		pending_instructors_info = []
		for pending_instructor in all_pending_instructors:
			deny_link = domain+reverse('deny-instructor', kwargs={'instructor_id':urlsafe_base64_encode(force_bytes(pending_instructor.id))})
			pending_instructors_info.append((pending_instructor.profile.profile_pic.url, pending_instructor.profile.get_fullname(), pending_instructor.id, domain+reverse('accept-instructor', kwargs={'instructor_id':urlsafe_base64_encode(force_bytes(pending_instructor.pk))}), deny_link))
		
		pending_instructors_info_page = request.GET.get('pi_page', 1)
		pending_instructors_info_paginator = Paginator(pending_instructors_info, 20)

		try:
			pending_instructors_info_sp = pending_instructors_info_paginator.page(pending_instructors_info_page)
		except PageNotAnInteger:
			pending_instructors_info_sp = pending_instructors_info_paginator.page(1)
		except EmptyPage:
			pending_instructors_info_sp = pending_instructors_info_paginator.page(pending_instrucstor_info_paginator.num_pages)

		admins_info = []
		for admin in Admin.objects.get(model_name='announcement').admins.all():
			admins_info.append((admin.profile.profile_pic.url, admin.profile.get_fullname(), admin.id))

		context = {
			'announcements_link':announcements_link,
			'instructors_link':instructors_link,
			'pending_instructors_link':pending_instructors_link,
			'pending_instructors_info_sp':pending_instructors_info_sp,
			'admins_info':admins_info,
			'is_admin':Admin.objects.get(model_name='announcement').admins.all().filter(pk=request.user.id).exists()
		}

		return render(request, 'lms_admin/pending_instructors.html', context)

@login_required
def accept_instructor_view(request, instructor_id):
	try:
		decoded_instructor_id = force_bytes(urlsafe_base64_decode(instructor_id))
		specific_instructor = User.objects.get(pk=decoded_instructor_id)
	except(User.DoesNotExist):
		specific_instructor = None
	messages = []
	errors = []
	if specific_instructor is not None:
		specific_instructor_fullname = specific_instructor.profile.get_fullname()
		# check if the user is an admin
		if Admin.objects.get(model_name='announcement').admins.all().filter(pk=request.user.id).exists():
			# check if the speicifc isntructor is not already an instructor
			if not specific_instructor.profile.is_instructor:
				# check if the specific instructor is on the pending list
				if Admin.objects.get(model_name='announcement').pending_instructors.all().filter(pk=specific_instructor.id).exists():
					# make the specific instructo
					specific_instructor.profile.is_instructor = True
					specific_instructor.profile.save()
					# remove the specific instructor on the pending list
					Admin.objects.get(model_name='announcement').pending_instructors.remove(specific_instructor)
					# send email to nptify the user that his/her request has been approved
					email_subject = 'Instructorship Request Accepted'
					body = f'Hi {specific_instructor_fullname}, your instructorship request has been approved\nYou can now create your own classes'
					receiver_email = [specific_instructor.email]
					send_email_task.delay(email_subject, body, receiver_email)
					messages.append(f"'{specific_instructor_fullname}' is now an instructor.")
				else:
					errors.append(f"'{specific_instructor_fullname}' is not on the list")
			else:
				errors.append(f"'{specific_instructor_fullname}' is already an instructor")
		else:
			return redirect('home')
	else:
		errors.append('USER DOES NOT EXIST')

	context = {
		'errors':errors,
		'messages':messages,
		'go_back_link':'http://'+get_current_site(request).domain + reverse('pending-instructors')
	}

	return render(request, 'learner_management/confirmation.html', context)

@login_required
def revoke_instructorship_view(request, instructor_id):
	try:
		decoded_instructor_id = force_bytes(urlsafe_base64_decode(instructor_id))
		specific_instructor = User.objects.get(pk=decoded_instructor_id)
	except(User.DoesNotExist):
		specific_instructor = None
	messages = []
	errors = []
	if specific_instructor is not None:
		specific_instructor_fullname = specific_instructor.profile.get_fullname()
		# check if the user is an admin
		if Admin.objects.get(model_name='announcement').admins.all().filter(pk=request.user.id).exists():
			# check if the speicifc isntructor is an instructor
			if specific_instructor.profile.is_instructor:
				# make the specific instructo
				specific_instructor.profile.is_instructor = False
				specific_instructor.profile.save()
				# notify the user that his/her instructorship has been revoked
				email_subject = 'Instructorship Revoked'
				body = f'Your Instructorship has been revoked.\nFor any inquiries please contact the administrators.\n'
				# extract the admin information
				for admin in Admin.objects.get(model_name='announcement').admins.all():
					name = admin.profile.get_fullname
					email = admin.email
					body += f'{name}: {email}\n'
				receiver_email = [specific_instructor.email]
				send_email_task(email_subject, body, receiver_email)
				messages.append(f"'{specific_instructor_fullname}' is no longer an instructor.")
			else:
				errors.append(f"'{specific_instructor_fullname}' is not an instructor")
		else:
			return redirect('home')
	else:
		errors.append('USER DOES NOT EXIST')

	context = {
		'errors':errors,
		'messages':messages,
		'go_back_link':'http://'+get_current_site(request).domain + reverse('instructors')
	}

	return render(request, 'learner_management/confirmation.html', context)

@login_required
def deny_instructor_view(request, instructor_id):
	try:
		decoded_instructor_id = force_bytes(urlsafe_base64_decode(instructor_id))
		specific_instructor = User.objects.get(pk=decoded_instructor_id)
	except(User.DoesNotExist):
		specific_instructor = None
	messages = []
	errors = []
	if specific_instructor is not None:
		specific_instructor_fullname = specific_instructor.profile.get_fullname()
		# check if the user is an admin
		if Admin.objects.get(model_name='announcement').admins.all().filter(pk=request.user.id).exists():
			# check if the speicifc isntructor is not already an instructor
			if not specific_instructor.profile.is_instructor:
				# check if the specific instructor is on the pending list
				if Admin.objects.get(model_name='announcement').pending_instructors.all().filter(pk=specific_instructor.id).exists():
					# remove the specific instructor on the pending list
					Admin.objects.get(model_name='announcement').pending_instructors.remove(specific_instructor)
					# notify the user that his/her instructorship request has been denied
					email_subject = 'Instructorship Denied'
					body = f'Your Instructorship request has been denied.\nFor any inquiries please contact the administrators.\n'
					# extract the admin information
					for admin in Admin.objects.get(model_name='announcement').admins.all():
						name = admin.profile.get_fullname
						email = admin.email
						body += f'{name}: {email}\n'
					receiver_email = [specific_instructor.email]
					send_email_task(email_subject, body, receiver_email)
					messages.append(f"'{specific_instructor_fullname}' instructorship is now denied.")
				else:
					errors.append(f"'{specific_instructor_fullname}' is not on the list")
			else:
				errors.append(f"'{specific_instructor_fullname}' is already an instructor")
		else:
			return redirect('home')
	else:
		errors.append('USER DOES NOT EXIST')

	context = {
		'errors':errors,
		'messages':messages,
		'go_back_link':'http://'+get_current_site(request).domain + reverse('pending-instructors')
	}

	return render(request, 'learner_management/confirmation.html', context)



@login_required
def announcement_showcase_view(request):
	# get the most latest announcement
	latest_announcement = Announcement.objects.latest('timestamp')

	announcement_images_info = []
	active_image = ''
	# get the name of the file and there link
	index = 0;
	for announcement_image in latest_announcement.announcementimages.all():
		lfi = (announcement_image.image.name, announcement_image.image.url, index)
		announcement_images_info.append(lfi)
		index+=1

	if len(announcement_images_info)>0:
		active_image = announcement_images_info.pop(0)

	context = {
		'announcement':latest_announcement,
		'announcement_images_info':announcement_images_info,
		'active_image':active_image

	}
	return render(request, 'lms_admin/announcement_showcase.html', context)

@login_required
def edit_announcement_view(request, announcement_id):
	try:
		decoded_announcement_id = force_bytes(urlsafe_base64_decode(announcement_id))
		specific_announcement = Announcement.objects.get(pk=decoded_announcement_id)
	except(Announcement.DoesNotExist):
		specific_announcement = None
	errors = []
	sucess = []
	if specific_announcement is not None:
		if Admin.objects.get(model_name='announcement').admins.all().filter(pk=request.user.id).exists():
			form = EditAnnouncementForm(instance=specific_announcement)
			if request.method == 'POST':
				form = EditAnnouncementForm(request.POST, instance=specific_announcement)
				if form.is_valid():
					form.save()
					return redirect('specific-announcement', announcement_id=announcement_id)
	context = {
		'sucess':sucess,
		'errors':errors,
		'form':form,
		'announcement':specific_announcement
	}

	return render(request, 'lms_admin/edit_announcement.html', context)

@login_required
def delete_announcement_view(request, announcement_id):
	try:
		decoded_announcement_id = force_bytes(urlsafe_base64_decode(announcement_id))
		specific_announcement = Announcement.objects.get(pk=decoded_announcement_id)
	except(Announcement.DoesNotExist):
		specific_announcement = None
	errors = []
	messages = []
	if specific_announcement is not None:
		# check if the user that is requesting is the instructor of the class that the lesson belong'
		if Admin.objects.get(model_name='announcement').admins.all().filter(pk=request.user.id).exists():
			specific_announcement_title = specific_announcement.title
			specific_announcement.delete()
			messages.append(f'Announcement: {specific_announcement_title} has been successfully deleted.')
		else:
			errors.append('You are the instructor of this class. So cannot delete this lesson')
	else:
		errors.append('Announcement DOES NOT EXIST')

	context = {
		'errors':errors,
		'messages':messages,
		'go_back_link':'http://'+get_current_site(request).domain+reverse('my-announcements')
	}

	return render(request, 'learner_management/confirmation.html', context)

@login_required
def request_instructorship_view(request):
	errors = []
	messages = []
	# check if the user is not yet an instructor
	if not request.user.profile.is_instructor:
		user_fullname = request.user.profile.get_fullname()
		# check if the user has not yet requested for instructorship
		if not Admin.objects.get(model_name='announcement').pending_instructors.all().filter(pk=request.user.pk).exists():
			Admin.objects.get(model_name='announcement').pending_instructors.add(request.user)
			# notify the administrators that this user wants to be an instructor
			email_subject = 'Instructorship Request'
			body = f'User {user_fullname} is requesting to be an instructor.'
			receiver_email = [admin.email for admin in Admin.objects.get(model_name='announcement').admins.all()]
			send_email_task(email_subject, body, receiver_email)
			messages.append('Your request is being processed, please wait until further notice')
		else:
			errors.append('You already requested to be an instructor, plese wait until further notice')
	else:
		errors.append('You are an instructor, so you no longer need this request')

	context = {
		'errors':errors,
		'messages':messages,
		'go_back_link':'http://'+get_current_site(request).domain+reverse('edit_profile')
	}

	return render(request, 'learner_management/confirmation.html', context)
