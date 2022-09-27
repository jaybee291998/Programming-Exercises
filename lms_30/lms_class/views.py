from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import LMSClassForm, StudentInviteForm, DeleteClassForm, UpdateClassBannerForm
#models
from .models import LMSClass, LMSClassInfo
# libraries needed to encode and decode id's
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

from django.urls import reverse
from django.contrib.auth import get_user_model
# the user model
User = get_user_model()
#for token generation
import random

#stuffs needed for email
from django.core.mail import EmailMessage
from django.conf import settings

# dependencies on other models
from lms_lesson.models import Lesson, Lecture
from lms_studentwork.models import StudentWork 

# for json response
from django.http import JsonResponse
import json

# to confirm if the password provided by the user is correct
from django.contrib.auth import authenticate

# to send mail async
from lms.task import send_email_task

# Create your views here.

template_dir = 'learner_management/'

@login_required
def createclass_view(request):
	template = 'home/home.html'
	form = LMSClassForm()
	if request.user.profile.is_instructor:
		template = 'learner_management/create_class.html'
		
		if request.method == 'POST':
			form = LMSClassForm(request.POST)
			if form.is_valid():
				# check if the new class is a duplicate of an existing class taugth by same instructor
				is_class_duplicate = False
				for lmsclass in request.user.classes_taugth.all(): #Lc.objects.filter(instructor=request.user):
					if form.cleaned_data.get('name')==lmsclass.name and form.cleaned_data.get('description')==lmsclass.description:
						is_class_duplicate = True
						break
				if not is_class_duplicate:
					a = form.save(commit=False)
					random_number = random.randint(1000000000, 9999999999)
					a.instructor = request.user
					# generate a unique token for the class
					hashed_info = hash(hash(request.user.email)+hash(random_number)+hash(form.cleaned_data.get('name'))+hash(form.cleaned_data.get('description')))
					class_token = hashed_info
					if hashed_info < 0:
						class_token = -1 * hashed_info
					a.class_token = class_token
					a.save()
					# create the class info
					LMSClassInfo.objects.create(lmsclass=a)
					return redirect('myclasses_view')
				else:
					return redirect('myclasses_view')
	else:
		return redirect('home')

	context = {
		'form':form

	}
	return render(request, template, context)



@login_required
def myclasses_view(request):
	my_classes = ''
	account_type = ''
	class_info = []
	if request.user.profile.is_instructor:
		my_classes = request.user.classes_taugth.all() #Lc.objects.filter(instructor = request.user)
		account_type = 'instructor'
	else:
		my_classes = request.user.classes.all() #Lc.objects.filter(students = request.user)
		account_type = 'student'

	# encode the class id
	domain = 'http://'+get_current_site(request).domain
	print(my_classes)
	print(request.user.classes_taugth)
	print(request.user)
	for specific_class in my_classes:
		link = reverse('specific-class-stream', kwargs={'class_id':urlsafe_base64_encode(force_bytes(specific_class.pk))})
		if specific_class.lesson.all().exists():
			upcoming_activity = specific_class.lesson.all().latest('deadline')
			upcoming_activity_link = domain+reverse('specific-lesson', kwargs={'lesson_id':urlsafe_base64_encode(force_bytes(upcoming_activity.pk))})
		else:
			upcoming_activity = None
			upcoming_activity_link = '#'
		ci = (specific_class, domain+link, specific_class.instructor.email, specific_class.lmsclassinfo.banner_bg.url, upcoming_activity, upcoming_activity_link)
		class_info.append(ci)
	context = {
		'class_info':class_info,
		'account_type':account_type,
		'create_class_link':domain+reverse('create-class'),
		'is_instructor':request.user.profile.is_instructor
	}

	return render(request, 'learner_management/myclasses.html', context)

@login_required
def delete_class_view(request, class_id):
	try:
		decoded_class_id = force_bytes(urlsafe_base64_decode(class_id))
		specific_class = LMSClass.objects.get(pk=decoded_class_id)

	except(LMSClass.DoesNotExist):
		specific_class = None
	messages = []
	errors = []
	form = DeleteClassForm()
	if specific_class is not None:
		if request.user == specific_class.instructor:
			if request.method == 'POST':
				form = DeleteClassForm(request.POST)
				if form.is_valid():
					user = authenticate(email=request.user.email, password=form.cleaned_data.get('password'))
					if request.user == user:
						messages.append('Yatta you can delete this class')
						specific_class.delete()
						context = {
							'messages':messages,
							'errors':errors,
							'go_back_link':'http://'+get_current_site(request).domain + reverse('home')
						}
						return render(request, 'learner_management/confirmation.html', context)
					else:
						errors.append('You cannot delete this class, because the password you provided is incorrect')
		else:
			errors.append('You are not the instructor of this class')
	else:
		errors.append('CLASS DOES NOT EXIST')

	context = {
		'messages':messages,
		'errors':errors,
		'form':form,
		'class':specific_class,
		'go_back_link':'http://'+get_current_site(request).domain+reverse('specific-class-stream', kwargs={'class_id':class_id})
	}

	return render(request, 'learner_management/delete_class.html', context)


@login_required
def specificclass_view(request, class_id, *args, **kwargs):
	try:
		decoded_class_id = force_text(urlsafe_base64_decode(class_id))
		specific_class = LMSClass.objects.get(pk=decoded_class_id)
	except(TypeError, ValueError, OverflowError, LMSClass.DoesNotExist):
		specific_class = None

	template = 'home/home.html'
	lessons_info = []

	if specific_class is not None:
		# check to see if the user is a student of the class or the instructor
		if request.user in specific_class.students.all() or specific_class.instructor == request.user:
			template = 'learner_management/specific_class.html'
			invite_student_link = 'http://'+get_current_site(request).domain + reverse('invite-student', kwargs={'class_id':class_id})
			add_new_lesson_link = 'http://'+get_current_site(request).domain + reverse('add-new-lesson', kwargs={'class_id':class_id})
			grade_sheet_link = 'http://'+get_current_site(request).domain + reverse('grade_sheet', kwargs={'class_id':class_id})
			# get all the lesson for the specific class
			domain = 'http://'+get_current_site(request).domain
			all_lessons = Lesson.objects.filter(lesson_class=specific_class)
			for lesson in all_lessons:
				lesson_link = reverse('specific-lesson', kwargs={'lesson_id':urlsafe_base64_encode(force_bytes(lesson.pk))})
				li = (lesson.title, domain+lesson_link)
				lessons_info.append(li)
		else:
			return redirect('home')
	context = {
		'class':specific_class,
		'students':specific_class.students.all(),
		'invite_link':invite_student_link,
		'add_new_lesson_link':add_new_lesson_link,
		'grade_sheet_link':grade_sheet_link,
		'lessons_info':lessons_info
	}

	return render(request, template, context)

# STREAM VIEW
@login_required
def specificclass_stream_view(request, class_id, *args, **kwargs):
	try:
		decoded_class_id = force_text(urlsafe_base64_decode(class_id))
		specific_class = LMSClass.objects.get(pk=decoded_class_id)
	except(TypeError, ValueError, OverflowError, LMSClass.DoesNotExist):
		specific_class = None

	template = 'home/home.html'
	lessons_and_lecture_info = []

	if specific_class is not None:
		# check to see if the user is a student of the class or the instructor
		if request.user in specific_class.students.all() or specific_class.instructor == request.user:
			template = 'learner_management/specific_class_stream.html'
			domain = 'http://'+get_current_site(request).domain
			# links
			stream_link = domain+reverse('specific-class-stream', kwargs={'class_id':class_id})
			classwork_link = domain+reverse('specific-class-classwork', kwargs={'class_id':class_id})
			people_link = domain+reverse('specific-class-people', kwargs={'class_id':class_id})
			grade_link = 'http://'+get_current_site(request).domain + reverse('specific-class-grade', kwargs={'class_id':class_id})
			change_banner_link = domain + reverse('change-banner', kwargs={'class_id':class_id})
			all_lessons = Lesson.objects.filter(lesson_class=specific_class)
			for lesson in all_lessons:
				lesson_link = reverse('specific-lesson', kwargs={'lesson_id':urlsafe_base64_encode(force_bytes(lesson.pk))})
				li = (lesson.title, domain+lesson_link, lesson.type_of_lesson, lesson.deadline, lesson.timestamp, 'lesson')
				lessons_and_lecture_info.append(li)
			all_lectures = Lecture.objects.filter(lecture_class=specific_class)
			for lecture in all_lectures:
				lecture_link = reverse('specific-lecture', kwargs={'lecture_id':urlsafe_base64_encode(force_bytes(lecture.pk))})
				li = (lecture.title, domain+lecture_link, lecture.type_of_lecture, 'No deadline', lecture.timestamp, 'lecture', lecture.description, specific_class.instructor.profile.get_fullname(), specific_class.instructor.profile.profile_pic.url)
				lessons_and_lecture_info.append(li)	

			lessons_and_lecture_info.sort(key=lambda a:a[4], reverse=True)
			# new = sorted(lessons_and_lecture_info, key=get_key, reverse=True)
			# print(new)
			# print(lessons_and_lecture_info)
		else:
			return redirect('home')
	context = {
		'stream_link':stream_link,
		'classwork_link':classwork_link,
		'people_link':people_link,
		'grade_link':grade_link,
		'change_banner_link':change_banner_link,
		'class':specific_class,
		'lessons_and_lecture_info':lessons_and_lecture_info,
		'is_instructor':request.user == specific_class.instructor,
		'delete_class_link':domain+reverse('delete-class', kwargs={'class_id':class_id}),
		'add_lecture_link':domain+reverse('add-lecture', kwargs={'class_id':class_id, 'type_of_lecture':urlsafe_base64_encode(force_bytes('lecture'))}),
		'add_announcement_link':domain+reverse('add-lecture', kwargs={'class_id':class_id, 'type_of_lecture':urlsafe_base64_encode(force_bytes('announcement'))})
		# 'logo':domain+'/media/logo/exam-logo.png'
	}

	return render(request, template, context)

# helper function
def get_key(li):
	return li[4]

# classwork
@login_required
def specificclass_classwork_view(request, class_id, *args, **kwargs):
	try:
		decoded_class_id = force_text(urlsafe_base64_decode(class_id))
		specific_class = LMSClass.objects.get(pk=decoded_class_id)
	except(TypeError, ValueError, OverflowError, LMSClass.DoesNotExist):
		specific_class = None

	template = 'home/home.html'
	lessons_info = []

	if specific_class is not None:
		# check to see if the user is a student of the class or the instructor
		if request.user in specific_class.students.all() or specific_class.instructor == request.user:
			template = 'learner_management/specific_class_classwork.html'
			domain = 'http://'+get_current_site(request).domain

			stream_link = domain+reverse('specific-class-stream', kwargs={'class_id':class_id})
			classwork_link = domain+reverse('specific-class-classwork', kwargs={'class_id':class_id})
			people_link = domain+reverse('specific-class-people', kwargs={'class_id':class_id})
			grade_link = 'http://'+get_current_site(request).domain + reverse('specific-class-grade', kwargs={'class_id':class_id})
			add_new_lesson_link = 'http://'+get_current_site(request).domain + reverse('add-new-lesson', kwargs={'class_id':class_id})

			all_lessons = Lesson.objects.filter(lesson_class=specific_class)
			for lesson in all_lessons:
				# number of sutdents that have handed in
				handed_in = len(lesson.studentwork.filter(turned_in=True));
				# number of student work that has been graded
				graded = len(lesson.studentwork.filter(graded=True));
				# number of students that submitted late
				late = len(lesson.studentwork.filter(late=True, turned_in=True))
				# number of students that has a missing work
				missing = len(lesson.studentwork.filter(late=True, turned_in=False))
				lesson_link = reverse('specific-lesson', kwargs={'lesson_id':urlsafe_base64_encode(force_bytes(lesson.pk))})


				# for a student check the status of the lesson
				status = ''
				if not request.user.profile.is_instructor:
					student_work = lesson.studentwork.get(student=request.user)
					if not student_work.turned_in and student_work.late:
						status = 'Missing'
					elif student_work.graded:
						status = 'Marked'
					elif student_work.turned_in:
						status = 'Handed in'
					else:
						status = 'Assigned'
				li = (lesson.title, domain+lesson_link, lesson.type_of_lesson, lesson.deadline, lesson.description, lesson.lessonfile.all(), lesson.id, lesson.timestamp, lesson.num, handed_in, graded, late, missing, status)
				lessons_info.append(li)
			lessons_info.sort(key=lambda a:a[7], reverse=True)


		else:
			return redirect('home')
	context = {
		'stream_link':stream_link,
		'classwork_link':classwork_link,
		'people_link':people_link,
		'grade_link':grade_link,
		'add_new_lesson_link':add_new_lesson_link,
		'class':specific_class,
		'lessons_info':lessons_info,
		'is_instructor':request.user == specific_class.instructor,
		'assigned':len(specific_class.students.all())
	}

	return render(request, template, context)

@login_required
def specificclass_people_view(request, class_id, *args, **kwargs):
	try:
		decoded_class_id = force_text(urlsafe_base64_decode(class_id))
		specific_class = LMSClass.objects.get(pk=decoded_class_id)
	except(TypeError, ValueError, OverflowError, LMSClass.DoesNotExist):
		specific_class = None

	template = 'home/home.html'
	lessons_info = []

	if specific_class is not None:
		# check to see if the user is a student of the class or the instructor
		if specific_class.students.all().filter(pk=request.user.id).exists() or specific_class.instructor == request.user:
			template = 'learner_management/specific_class_people.html'
			invite_student_link = 'http://'+get_current_site(request).domain + reverse('invite-student', kwargs={'class_id':class_id})

			# get all the lesson for the specific class
			domain = 'http://'+get_current_site(request).domain
			

			stream_link = domain+reverse('specific-class-stream', kwargs={'class_id':class_id})
			classwork_link = domain+reverse('specific-class-classwork', kwargs={'class_id':class_id})
			people_link = domain+reverse('specific-class-people', kwargs={'class_id':class_id})
			grade_link = 'http://'+get_current_site(request).domain + reverse('specific-class-grade', kwargs={'class_id':class_id})

			instructor_info = (specific_class.instructor.profile.profile_pic.url, specific_class.instructor.profile.first_name + ' ' + specific_class.instructor.profile.last_name)
			students_info = []
			for student in specific_class.students.all():
				si = (student.profile.profile_pic.url, student.profile.first_name+ ' ' + student.profile.last_name, student.id, domain+reverse('unenroll-student', kwargs={'class_id':class_id, 'student_id':urlsafe_base64_encode(force_bytes(student.id))}))
				students_info.append(si)

			pending_students_info = []
			for student in specific_class.pending_students.all():
				accept_student_link = domain+reverse('accept-student', kwargs={'class_id':class_id, 'class_token':specific_class.class_token, 'student_id':urlsafe_base64_encode(force_bytes(student.id))})
				pending_students_info.append((student.profile.profile_pic.url, student.profile.first_name+ ' ' + student.profile.last_name, accept_student_link))

			invited_students_info = []
			for student in specific_class.invited_students.all():
				invited_students_info.append((student.profile.profile_pic.url, student.profile.first_name+ ' ' + student.profile.last_name))



		else:
			return redirect('home')
	context = {
		'stream_link':stream_link,
		'classwork_link':classwork_link,
		'people_link':people_link,
		'grade_link':grade_link,
		'class':specific_class,
		'instructor_info': instructor_info,
		'students_info':students_info,
		'is_instructor': request.user == specific_class.instructor,
		'pending_students_info': pending_students_info,
		'invited_students_info': invited_students_info,
		'invite_link':invite_student_link,
		'empty_invited_students':len(invited_students_info)==0,
		'empty_pending_students':len(pending_students_info)==0
	}

	return render(request, template, context)

@login_required
def specificclass_grade_view(request, class_id, *args, **kwargs):
	try:
		decoded_class_id = force_text(urlsafe_base64_decode(class_id))
		specific_class = LMSClass.objects.get(pk=decoded_class_id)
	except(TypeError, ValueError, OverflowError, LMSClass.DoesNotExist):
		specific_class = None

	template = 'home/home.html'
	lessons_info = []

	if specific_class is not None:
		# check to see if the user is a student of the class or the instructor
		if request.user in specific_class.students.all() or specific_class.instructor == request.user:
			# get all the lesson for the specific class
			domain = 'http://'+get_current_site(request).domain
			template = 'learner_management/specific_class_grade.html'
			stream_link = domain+reverse('specific-class-stream', kwargs={'class_id':class_id})
			classwork_link = domain+reverse('specific-class-classwork', kwargs={'class_id':class_id})
			people_link = domain+reverse('specific-class-people', kwargs={'class_id':class_id})
			grade_link = 'http://'+get_current_site(request).domain + reverse('specific-class-grade', kwargs={'class_id':class_id})
		else:
			return redirect('home')
	context = {
		'stream_link':stream_link,
		'classwork_link':classwork_link,
		'people_link':people_link,
		'grade_link':grade_link,
		'class':specific_class,
		'class_id':class_id
		# 'grade_sheet_link':grade_sheet_link,
	}

	return render(request, template, context)



@login_required
def invite_student_view(request, class_id, *args, **kwargs):
	link = "Your not the instructor of this class"
	form = StudentInviteForm()
	try:
		decoded_class_id = force_text(urlsafe_base64_decode(class_id))
		specific_class = LMSClass.objects.get(pk=decoded_class_id)
	except(TypeError, ValueError, OverflowError, LMSClass.DoesNotExist):
		specific_class = None

	template = 'home/home.html'
	errors = []

	if specific_class is not None:
		#check to see if the user is an instructor and the instructor of the specific class
		if request.user.profile.is_instructor and specific_class.instructor == request.user:
			#generate the link based on the class token
			link = 'http://'+get_current_site(request).domain + reverse('join-class', kwargs={'class_id':class_id, 'class_token':specific_class.class_token})
			# search_link = 'http://'+get_current_site(request).domain + reverse()
			if request.method == 'POST':
				form = StudentInviteForm(request.POST)
				if form.is_valid():
					invited_student = User.objects.get(email=form.cleaned_data.get('email'))
					#check if the invited student has not request to join yet
					if not specific_class.pending_students.all().filter(pk=invited_student.id).exists():
						# check if the invited student is not yet a student in the class
						if not specific_class.students.all().filter(pk=invited_student.id).exists():
							invited_student_encrypted_id = urlsafe_base64_encode(force_bytes(invited_student.pk))
							invited_student_link = 'http://'+get_current_site(request).domain + reverse('accept-invite', kwargs={'class_id':class_id, 'class_token':specific_class.class_token, 'student_id':invited_student_encrypted_id})
							email_subject = 'Class Invitation'
							body = "Hi {student_name}, {instructor_name} is inviting you to his/her class '{class_title}-{class_description}'.\n".format(student_name=invited_student.profile.first_name + " " + invited_student.profile.last_name, class_title=specific_class.name, class_description=specific_class.description, instructor_name=request.user.profile.first_name + " " + request.user.profile.last_name)
							body += "Here is his/her message\n'{instructor_message}'\n".format(instructor_message=form.cleaned_data.get('message'))
							body += "Click this link join the class\nLink: {link}".format(link=invited_student_link)
							sender_email = settings.EMAIL_HOST_USER
							receiver_email = [form.cleaned_data.get('email')]
							# send email async
							send_email_task.delay(email_subject, body, receiver_email)
							# add the invited student to the invited student list
							specific_class.invited_students.add(invited_student)
							return redirect('myclasses_view')
						else:
							errors.append('You no longer need to invite this student, because he/she is already in your class')
					else:
						errors.append('You dont need to invite this student anymore, because this student has already requested to join your class')
		else:
			return redirect('myclasses_view')
	else:
		return redirect('myclasses_view')
					
	context = {
		'link':link,
		'form':form,
		'errors':errors,
		'student_search_link':'http://'+get_current_site(request).domain+reverse('student-search')
	}

	return render(request, 'learner_management/invite_student.html', context)

@login_required
def accept_invite_view(request, class_id, class_token, student_id):
	errors = []
	sucess = []
	try:
		decoded_student_id = force_bytes(urlsafe_base64_decode(student_id))
		decoded_class_id = force_bytes(urlsafe_base64_decode(class_id))

		specific_class = LMSClass.objects.get(pk=decoded_class_id)
		specific_student = User.objects.get(pk=decoded_student_id)
	except(TypeError, ValueError, OverflowError, LMSClass.DoesNotExist, User.DoesNotExist):
		specific_class = None
		specific_student = None
	# check to see if the given class id and student id is valid
	if specific_class is not None and specific_student is not None:
		# check to see if the given token matches the class tokeb
		if specific_class.class_token == class_token:
			# check to see if the logged in user is the invited user
			if request.user == specific_student:
				# check to see if the student to be added id not already in the students list of the class
				if not specific_student in specific_class.students.all():
					# check to see if the student is in the invited lis
					if specific_class.invited_students.all().filter(pk=specific_student.id).exists():
						specific_class.students.add(specific_student)
						assign_student_work(specific_student, specific_class)
						sucess.append('sucess you are now added to the class')
						# send a message to the instructor that the invited student accepted his/her invitation
						email_subject = 'Invite Accepted'
						body = "{student_name} accepted your invitation to join your class '{class_name}'".format(student_name=specific_student.profile.get_fullname(), class_name=specific_class.name)
						sender_email = settings.EMAIL_HOST_USER
						receiver_email = [specific_class.instructor.email]
						# send mail async
						send_email_task.delay(email_subject, body, receiver_email)
						#email = EmailMessage(
						#	email_subject,
						#	body,
						#	sender_email,
						#	receiver_email
						#)
						#email.fail_silenty=False 
						#email.send()

						# remove the student in the invited list
						specific_class.invited_students.remove(specific_student)
						return redirect('myclasses_view')
					else:
						errors.append('You are not invited in this class')
				else:
					errors.append('You are already in the class, you no longer need to join')
			else:
				errors.append('This link is inviting another student, not you.')
		else:
			errors.append('Token mismatch')
	else:
		errors.append('Invalid Link')
		return redirect('home')


	context={
		'class_id':class_id,
		'class_token':class_token,
		'student_id':student_id,
		'errors': errors,
		'sucess':sucess
	}
	return render(request, 'learner_management/accept_invite.html', context)

@login_required
def join_class_view(request, class_id, class_token):
	try:
		decoded_class_id = force_bytes(urlsafe_base64_decode(class_id))
		specific_class = LMSClass.objects.get(pk=decoded_class_id)
	except(TypeError, ValueError, OverflowError, LMSClass.DoesNotExist):
		specific_class = None
	errors = []
	messages = []
	if specific_class is not None:
		# check to see if the user that is requesting is not an intructor
		if not request.user.profile.is_instructor:
			#check to see if the joining student is not yet on the class
			if not specific_class.students.all().filter(id=request.user.id).exists():
				# check to see if the joining student is not already on the pending list
				if not specific_class.pending_students.all().filter(id=request.user.id).exists():
					# check to see if the student is not already been invited to the class
					if not specific_class.invited_students.all().filter(pk=request.user.id).exists():
						# check if the provided class token matched with the class id
						if specific_class.class_token == class_token:
							specific_class.pending_students.add(request.user)
							# message the instrucstor that this student wants to join his/her class
							email_subject = 'Join Request'
							body = "{student_name} wants to join your class '{class_name}'\n".format(student_name=request.user.profile.get_fullname(), class_name=specific_class.name)
							body += "You can accept this request on the People tab in your class"
							sender_email = settings.EMAIL_HOST_USER
							receiver_email = [specific_class.instructor.email]
							# send mail async
							send_email_task.delay(email_subject, body, receiver_email)
							messages.append('Yatta your request is waiting for approval')
						else:
							errors.append('Class token does not match')
					else:
						errors.append('You no longer need to join this class, beacuse your are already invited. Please check your email inbox for the invitation link')
				else:
					errors.append('Your request is already being processed, you can not request another request')
			else:
				errors.append('You are already in this class, you no longer need to join')
		else:
			errors.append('You are an intructor, you can not join any class')

	context = {
		'messages': messages,
		'errors': errors
	}

	return render(request, 'learner_management/join_class.html', context)

@login_required
def accept_student_view(request, class_id, class_token, student_id):
	try:
		decoded_class_id = force_bytes(urlsafe_base64_decode(class_id))
		decoded_student_id = force_bytes(urlsafe_base64_decode(student_id))

		specific_class = LMSClass.objects.get(pk=decoded_class_id)
		specific_student = User.objects.get(pk=decoded_student_id)
	except(TypeError, ValueError, OverflowError, LMSClass.DoesNotExist, User.DoesNotExist):
		specific_class = None
		specific_student = None

	errors = []
	messages = []
	if specific_student is not None and specific_class is not None:
		# check to see if the user requesting the approval is the instructor of the specific class
		if request.user == specific_class.instructor:
			# check if the class token matched the the class token of the specific class
			if specific_class.class_token == class_token:
				# check to see if the specific student is on the pending list
				if specific_class.pending_students.all().filter(pk=specific_student.id).exists():
					# check to see if the specific student is not in the student list of the specific class
					if not specific_class.students.all().filter(pk=specific_student.id).exists():
						# remove the student from the pending list
						specific_class.pending_students.remove(specific_student)
						# add the specific student to the student list of the specific class
						specific_class.students.add(specific_student)
						# assign all the existing classwork tot the specific student
						assign_student_work(specific_student, specific_class)
						messages.append('Success, '+specific_student.profile.first_name+' '+specific_student.profile.last_name+' is now in your class')

						# send an email message to the student that has been accepted
						email_subject = 'Join Request Accepted'
						body = "Hi {student_name}, you have been accepted in the class '{class_title}'-\n'{class_description}'.\n".format(student_name=specific_student.profile.get_fullname(), class_title=specific_class.name, class_description=specific_class.description)
						body += 'You can now go to the class by following the link\n'
						body += 'Link: {link}'.format(link='http://'+get_current_site(request).domain+reverse('specific-class-stream', kwargs={'class_id':urlsafe_base64_encode(force_bytes(specific_class.id))}))
						sender_email = settings.EMAIL_HOST_USER
						receiver_email = [specific_student.email]
						send_email_task.delay(email_subject, body, receiver_email)
						# messages.append('Yatta you can apprve this request')
					else:
						errors.append('This student is already in the class')
				else:
					errors.append('This student have not requested to join your class')
			else:
				errors.append('Class token does not match')
		else:
			errors.append('You cannot approve this request')
	else:
		errors.append('Either the class or the student does not exist')

	context = {
		'messages':messages,
		'errors': errors
	}

	return render(request, 'learner_management/accept_student.html', context)


def unenroll_student_view(request, class_id, student_id):
	try:
		decoded_class_id = force_bytes(urlsafe_base64_decode(class_id))
		decoded_student_id = force_bytes(urlsafe_base64_decode(student_id))

		specific_class = LMSClass.objects.get(pk=decoded_class_id)
		specific_student = User.objects.get(pk=decoded_student_id)

	except(ValueError, TypeError, OverflowError, LMSClass.DoesNotExist, User.DoesNotExist):
		specific_class = None
		specific_student = None

	messages = []
	errors = []
	if specific_class is not None and specific_student is not None:
		if request.user == specific_class.instructor:
			if specific_class.students.all().filter(pk=specific_student.id).exists():
				# remove the student in the class' students list
				specific_class.students.remove(specific_student)

				# then delete of the students student works
				for lesson in specific_class.lesson.all():
					student_work_to_remove = lesson.studentwork.all().get(student=specific_student)
					student_work_to_remove.delete()
				full_name = specific_student.profile.first_name + ' ' + specific_student.profile.last_name
				messages.append(full_name + ' is now unenrolled in your class ' + specific_class.name)

				# send a message to the student that she/he has unenrolled
				email_subject = 'Class Unenrollment'
				body = "Hi {student_name}, you have been unenrolled/kicked-out in the class '{class_title}'".format(student_name=specific_student.profile.get_fullname(), class_title=specific_class.name, class_description=specific_class.description)
				body += 'You can inquire your questions with your instructor by sending an email on his/her email address\n'
				body += 'instructors email address: {email_add}'.format(email_add=specific_class.instructor.email)
				sender_email = settings.EMAIL_HOST_USER
				receiver_email = [specific_student.email]
				send_email_task.delay(email_subject, body, receiver_email)
			else:
				errors.append('This student is not on your class')
		else:
			errors.append('You are not allowed to do this action')
	else:
		errors.append('Invalid Request: The either or both class_id or student_id is invalid')

	context={
		'messages':messages,
		'errors':errors,
		'go_back_link':'http://'+get_current_site(request).domain+reverse('specific-class-people', kwargs={'class_id':class_id})
	}

	return render(request, 'learner_management/confirmation.html', context)


# @login_required
# def invite_student_no_form_view(request, class_id, *args, **kwargs):
# 	link = "Your not the instructor of this class"
# 	form = StudentInviteForm()
# 	try:
# 		decoded_class_id = force_text(urlsafe_base64_decode(class_id))
# 		specific_class = LMSClass.objects.get(pk=decoded_class_id)
# 	except(TypeError, ValueError, OverflowError, LMSClass.DoesNotExist):
# 		specific_class = None

# 	template = 'home/home.html'

# 	if specific_class is not None:
# 		#check to see if the user is an instructor and the instructor of the specific class
# 		if request.user.profile.is_instructor and specific_class.instructor == request.user:
# 			#generate the link based on the class token
# 			link = 'http://'+get_current_site(request).domain + reverse('join-class', kwargs={'class_id':class_id, 'class_token':specific_class.class_token})
# 			if request.method == 'POST':
# 				form = StudentInviteForm(request.POST)
# 				if form.is_valid():
# 					invited_student = User.objects.get(email=form.cleaned_data.get('email'))
# 					invited_student_encrypted_id = urlsafe_base64_encode(force_bytes(invited_student.pk))
# 					invited_student_link = 'http://'+get_current_site(request).domain + reverse('accept-invite', kwargs={'class_id':class_id, 'class_token':specific_class.class_token, 'student_id':invited_student_encrypted_id})
# 					email_subject = 'Class Invitation'
# 					body = "Hi {student_name}, {instructor_name} is inviting you to his/her class '{class_title}-{class_description}'.\n".format(student_name=invited_student.profile.first_name + " " + invited_student.profile.last_name, class_title=specific_class.name, class_description=specific_class.description, instructor_name=request.user.profile.first_name + " " + request.user.profile.last_name)
# 					body += "Here is his/her message\n'{instructor_message}'\n".format(instructor_message=form.cleaned_data.get('message'))
# 					body += "Click this link join the class\nLink: {link}".format(link=invited_student_link)
# 					sender_email = settings.EMAIL_HOST_USER
# 					receiver_email = [form.cleaned_data.get('email')]
# 					email = EmailMessage(
# 							email_subject,
# 							body,
# 							sender_email,
# 							receiver_email
# 						)
# 					email.fail_silenty=False 
# 					email.send()
# 					return redirect('myclasses_view')
# 		else:
# 			return redirect('myclasses_view')
# 	else:
# 		return redirect('myclasses_view')
					
# 	context = {
# 		'link':link,
# 		'form':form
# 	}

# 	return render(request, 'learner_management/invite_student.html', context)







def grade_sheet_view(request, class_id):
	try:
		decoded_class_id = force_bytes(urlsafe_base64_decode(class_id))
		specific_class = LMSClass.objects.get(pk=decoded_class_id)
	except(TypeError, ValueError, OverflowError, LMSClass.DoesNotExist):
		specific_class = None
	message = ['what in the']
	if specific_class is not None:
		if request.user == specific_class.instructor:
			class_students = specific_class.students.all()
			class_lessons = specific_class.lesson.all()
			students_grades = []
			for student in class_students:
				student_grade = [student.profile.first_name]
				for lesson in class_lessons:
					student_grade.append(StudentWork.objects.get(student=student, lesson=lesson).mark)
				students_grades.append(student_grade)
		else:
			message.append('your not the instructor of this class')
			return redirect('myclasses_view')
	else:
		message.append('class does not exist')
		return redirect('home')
	context = {
		'class_students':class_students,
		'class_lessons':class_lessons,
		'message':message,
		'students_grades':students_grades,
		'domain':'http://'+get_current_site(request).domain
	}	

	return render(request, 'learner_management/grade_sheet.html', context)	


# Helper functions
def assign_student_work(specific_student, specific_class):
	all_class_lessons = specific_class.lesson.all()
	for lesson in all_class_lessons:
		new_student_work = StudentWork(student=specific_student, lesson=lesson, mark=-1)
		new_student_work.save()


@login_required
def student_search_view(request):
	# if 'term' in request.GET:
	# 	term = request.GET.get('term')
	# 	qs = User.objects.filter(profile__first_name__istartswith=term) | User.objects.filter(profile__last_name__istartswith=term) | User.objects.filter(email__istartswith=term)
	# 	full_names = list()
	# 	for student in qs:
	# 		full_names.append(student.profile.first_name + " " + student.profile.last_name)
	# 	return JsonResponse(full_names, safe=False)
	if request.user.profile.is_instructor:
		return render(request, template_dir+'student_search.html', {'domain':'http://'+get_current_site(request).domain})
	return redirect('home')

@login_required
def search_view(request):
	if request.method=='POST':
		search_string = json.loads(request.body).get('searchText')

		qs = User.objects.filter(profile__first_name__istartswith=term) | User.objects.filter(profile__last_name__istartswith=term) | User.objects.filter(email__istartswith=term)

		data = qs.values()

		return JsonResponse(list(data), safe=False)

@login_required
def change_class_banner_view(request, class_id):
	try:
		decoded_class_id = force_bytes(urlsafe_base64_decode(class_id))
		specific_class_info = LMSClass.objects.get(pk=decoded_class_id).lmsclassinfo
	except(LMSClass.DoesNotExist):
		specific_class_info = None
	
	if specific_class_info is not None:
		if request.user == specific_class_info.lmsclass.instructor:

			form = UpdateClassBannerForm(instance=specific_class_info)
			domain = 'http://'+get_current_site(request).domain
			stream_link = domain+reverse('specific-class-stream', kwargs={'class_id':class_id})
			if request.method == 'POST':
				form = UpdateClassBannerForm(request.POST, request.FILES, instance=specific_class_info)
				if form.is_valid():
					form.save()
	context = {
		'stream_link':stream_link,
		'form':form,
		'class':specific_class_info.lmsclass
	}
	return render(request, 'learner_management/change_class_banner.html', context)