from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from .forms import AddNewLessonForm, AddLessonFileForm, EditLessonForm, AddLectureForm, AddLectureFileForm, EditLectureForm, LectureCommentForm

from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from django.contrib.auth import get_user_model
# the user model
User = get_user_model()

#stuffs needed for email
from django.core.mail import EmailMessage
from django.conf import settings


from lms.utils import check_duplicate_file
# Create your views here.

# other model dependencies
from lms_class.models import LMSClass
from .models import Lesson, LessonFile, Lecture, LectureFile, byte_to_mb
from lms_studentwork.models import StudentWork

# send mail async
from lms.task import send_email_task

@login_required
def add_new_lesson_view(request, class_id):
	form = AddNewLessonForm()
	errors = []
	sucess = []
	try:
		decoded_class_id = force_bytes(urlsafe_base64_decode(class_id))
		specific_class = LMSClass.objects.get(pk=decoded_class_id)
	except(TypeError, ValueError, OverflowError, LMSClass.DoesNotExist):
		specific_class = None

	if request.user.profile.is_instructor and specific_class.instructor == request.user:
		if specific_class is not None:
			if request.method == 'POST':
				form = AddNewLessonForm(request.POST)

				if form.is_valid():
					title = form.cleaned_data.get('title')
					description = form.cleaned_data.get('description')

					is_duplicate = False
					# get all the lessons of the specfic class
					all_lessons = specific_class.lesson.all() #Lesson.objects.filter(lesson_class=specific_class)
					# check all the lesson to see if the new lesson already exist
					for lesson in all_lessons:
						if lesson.title == title and lesson.description == description:
							is_duplicate = True
							break
					nums = []
					for lesson in all_lessons.filter(type_of_lesson=form.cleaned_data.get('type_of_lesson')):
						nums.append(lesson.num)
					# the subject has no duplicate
					if not is_duplicate:
						a = form.save(commit=False)
						a.lesson_class = specific_class
						a.num = max(nums)+1 if len(nums)>=1 else 0
						a.save()

						# create the corresponding student work for every student in the class
						all_students = specific_class.students.all()
						for student in all_students:
							new_student_work = StudentWork(student = student, lesson=a)
							new_student_work.save()
							# print(student)

						# after saving the new lesson 
						# email every student in the class that a new lesson has been
						# added to there class
						email_subject = 'New {type}'.format(type=a.type_of_lesson)
						body = "{instructor} posted a new {lesson_type}: '{title}' in {lmsclass}\nDue: {due}\nLesson link: {link}\n".format(instructor=specific_class.instructor.profile.get_fullname(), lesson_type=a.type_of_lesson, lmsclass=specific_class.name, due=a.deadline, title=a.title, link='http://'+get_current_site(request).domain+reverse('specific-lesson',kwargs={'lesson_id':urlsafe_base64_encode(force_bytes(a.id))}))
						body += "Instructions: '{instruction}'\n\n".format(instruction=a.description) 
						sender_email = settings.EMAIL_HOST_USER
						receiver_email = [student.email for student in specific_class.students.all()]
						send_email_task.delay(email_subject, body, receiver_email)
						sucess.append('new lesson added')
						return redirect('http://'+get_current_site(request).domain + reverse('add-lesson-file', kwargs={'lesson_id':urlsafe_base64_encode(force_bytes(a.pk))}))
					else:
						errors.append('lesson already exist')
				else:
					errors.append('Invalid Form')

		else:
			errors.append('Class does not exist')
	else:
		errors.append('You have no valid credential to add a new lesson to this class')
		return redirect('home')

	context = {
		'form':form,
		'errors':errors,
		'sucess':sucess
	}
	return render(request, 'learner_management/add_new_lesson.html', context)

@login_required
def add_lecture_view(request, class_id, type_of_lecture):
	try:
		decoded_class_id = force_bytes(urlsafe_base64_decode(class_id))
		decoded_type = force_bytes(urlsafe_base64_decode(type_of_lecture))
		print(type(decoded_type))
		if decoded_type == bytes('lecture', 'utf-8'):
			decoded_type = 'lecture'
		elif decoded_type == bytes('announcement', 'utf-8'):
			decoded_type = 'announcement'
		specific_class = LMSClass.objects.get(pk=decoded_class_id)
	except(LMSClass.DoesNotExist):
		specific_class = None

	if specific_class is not None:
		if request.user == specific_class.instructor:
			form = AddLectureForm()
			if request.method == 'POST':
				form = AddLectureForm(request.POST)
				if form.is_valid():
					a = form.save(commit=False)
					a.lecture_class = specific_class
					a.type_of_lecture = decoded_type
					a.save()
					email_subject = 'New {type}'.format(type=a.type_of_lecture)
					body = "{instructor} posted a new {lecture_type}: '{title}' in {lmsclass}\nLecture link: {link}\n".format(instructor=specific_class.instructor.profile.get_fullname(), lecture_type=a.type_of_lecture, lmsclass=specific_class.name, title=a.title, link='http://'+get_current_site(request).domain+reverse('specific-lecture',kwargs={'lecture_id':urlsafe_base64_encode(force_bytes(a.id))}))
					body += "Instructions: '{instruction}'\n\n".format(instruction=a.description) 
					receiver_email = [student.email for student in specific_class.students.all()]
					send_email_task.delay(email_subject, body, receiver_email)
					if decoded_type == 'lecture':
						return redirect('add-lecture-file', lecture_id=urlsafe_base64_encode(force_bytes(a.pk)))
					return redirect('specific-class-stream', class_id=class_id)
	context = {
		'form':form,
		'title':decoded_type
	}

	return render(request, 'learner_management/add_lecture.html', context)

@login_required
def add_lecture_file_view(request, lecture_id):
	try:
		decoded_lecture_id = force_bytes(urlsafe_base64_decode(lecture_id))
		specific_lecture = Lecture.objects.get(pk=decoded_lecture_id)
	except(TypeError, ValueError, OverflowError, Lecture.DoesNotExist):
		specific_lecture = None
	form = AddLectureFileForm()
	existing_lecture_files = []
	errors = []
	if specific_lecture is not None:
		existing_files = specific_lecture.lecturefile.all()
		combined_file_size = byte_to_mb(sum([existing_file.file.size for existing_file in existing_files]))
		if specific_lecture.lecture_class.instructor == request.user:
			form = AddLectureFileForm(request.POST, request.FILES)

			if request.method == 'POST':
				if form.is_valid():
					file_name = form.cleaned_data.get('file').name
					# check if the file being uploaded is already on the existing files
					if not check_duplicate_file(existing_files, form.cleaned_data.get('file')):
						file_size = byte_to_mb(form.cleaned_data.get('file').size)

						if file_size + combined_file_size < byte_to_mb(settings.MAX_COMBINED_FILE_SIZE):
							a = form.save(commit=False)
							a.lecture = specific_lecture
							a.save()
						else:
							errors.append(f'You exceeded the combined file size limit of {byte_to_mb(settings.MAX_COMBINED_FILE_SIZE)}mb, current combined size {combined_file_size}mb, you are trying to upload a file of size {file_size}mb')
					else:
						errors.append(f'The file {file_name} is already uploaded')
		else:
			return redirect('home')
	else:
		return redirect('home')

	if specific_lecture is not None:
		# get all the existing lesson files 
		 #LessonFile.objects.filter(lesson=specific_lesson)
		for existing_file in specific_lecture.lecturefile.all():
			delete_link = 'http://'+get_current_site(request).domain+reverse('delete-lecture-file', kwargs={'lecture_file_id':urlsafe_base64_encode(force_bytes(existing_file.id)), 'lecture_id':lecture_id})
			efi = (existing_file.file.name, existing_file.file.url, delete_link)
			existing_lecture_files.append(efi)

	context = {
		'form':form,
		'title':specific_lecture.title,
		'lecture_files_info':existing_lecture_files,
		'lecture_link': 'http://'+get_current_site(request).domain+reverse('specific-lecture', kwargs={'lecture_id':lecture_id}),
		'errors':errors,
		'combined_file_size':combined_file_size
	}

	return render(request, 'learner_management/add_lecture_file.html', context)

# edit the lesson
@login_required
def edit_lesson_view(request, lesson_id):
	try:
		decoded_lesson_id = force_bytes(urlsafe_base64_decode(lesson_id))
		specific_lesson = Lesson.objects.get(pk=decoded_lesson_id)
		specific_class = specific_lesson.lesson_class
	except(Lesson.DoesNotExist):
		specific_lesson = None
	errors = []
	sucess = []
	if specific_lesson is not None:
		if request.user == specific_lesson.lesson_class.instructor:
			form = EditLessonForm(instance=specific_lesson)
			if request.method == 'POST':
				form = EditLessonForm(request.POST, instance=specific_lesson)
				if form.is_valid():
					title = form.cleaned_data.get('title')
					description = form.cleaned_data.get('description')

					is_duplicate = False
					# get all the lessons of the specfic class
					all_lessons = specific_class.lesson.all() #Lesson.objects.filter(lesson_class=specific_class)
					# check all the lesson to see if the new lesson already exist
					for lesson in all_lessons:
						if lesson.title == title and lesson.description == description:
							if lesson != specific_lesson:
								is_duplicate = True
								break
					nums = []
					for lesson in all_lessons.filter(type_of_lesson=form.cleaned_data.get('type_of_lesson')):
						nums.append(lesson.num)
					# the subject has no duplicate
					if not is_duplicate:
						#check to see if the given number already exist among the list
						form.save()
						return redirect('specific-lesson', lesson_id=lesson_id)
					else:
						errors.append('Lesson already exist')
	context = {
		'sucess':sucess,
		'errors':errors,
		'form':form,
		'lesson':specific_lesson
	}

	return render(request, 'learner_management/edit_lesson.html', context)

# edit the lesson
@login_required
def edit_lecture_view(request, lecture_id):
	try:
		decoded_lecture_id = force_bytes(urlsafe_base64_decode(lecture_id))
		specific_lecture = Lecture.objects.get(pk=decoded_lecture_id)
		specific_class = specific_lecture.lecture_class
	except(Lecture.DoesNotExist):
		specific_lecture = None
	errors = []
	sucess = []
	if specific_lecture is not None:
		if request.user == specific_lecture.lecture_class.instructor:
			form = EditLectureForm(instance=specific_lecture)
			if request.method == 'POST':
				form = EditLectureForm(request.POST, instance=specific_lecture)
				if form.is_valid():
					form.save()
					return redirect('specific-lecture', lecture_id=lecture_id)
	context = {
		'sucess':sucess,
		'errors':errors,
		'form':form,
		'lecture':specific_lecture
	}

	return render(request, 'learner_management/edit_lecture.html', context)

@login_required
def delete_lesson(request, lesson_id):
	try:
		decoded_lesson_id = force_bytes(urlsafe_base64_decode(lesson_id))
		specific_lesson = Lesson.objects.get(pk=decoded_lesson_id)
	except(Lesson.DoesNotExist):
		specific_lesson = None
	errors = []
	messages = []
	if specific_lesson is not None:
		# check if the user that is requesting is the instructor of the class that the lesson belong'
		if request.user == specific_lesson.lesson_class.instructor:
			specific_lesson_info = (specific_lesson.title, specific_lesson.num, specific_lesson.type_of_lesson, specific_lesson.lesson_class.id)
			specific_lesson.delete()
			messages.append('{type_of_lesson}# {num}: {title} has been successfully deleted.'.format(type_of_lesson=specific_lesson_info[2], num=specific_lesson_info[1], title=specific_lesson_info[0]))
		else:
			errors.append('You are the instructor of this class. So cannot delete this lesson')
	else:
		errors.append('LESSON DOES NOT EXIST')

	context = {
		'errors':errors,
		'messages':messages,
		'go_back_link':'http://'+get_current_site(request).domain+reverse('specific-class-stream', kwargs={'class_id':urlsafe_base64_encode(force_bytes(specific_lesson_info[3]))})
	}

	return render(request, 'learner_management/confirmation.html', context)

@login_required
def delete_lecture(request, lecture_id):
	try:
		decoded_lecture_id = force_bytes(urlsafe_base64_decode(lecture_id))
		specific_lecture = Lecture.objects.get(pk=decoded_lecture_id)
	except(Lecture.DoesNotExist):
		specific_lecture = None
	errors = []
	messages = []
	if specific_lecture is not None:
		# check if the user that is requesting is the instructor of the class that the lesson belong'
		if request.user == specific_lecture.lecture_class.instructor:
			specific_lecture_info = (specific_lecture.title, specific_lecture.type_of_lecture, specific_lecture.lecture_class.id)
			specific_lecture.delete()
			messages.append('{type_of_lecture}: {title} has been successfully deleted.'.format(type_of_lecture=specific_lecture_info[1], title=specific_lecture_info[0]))
		else:
			errors.append('You are the instructor of this class. So cannot delete this lesson')
	else:
		errors.append('LECTURE DOES NOT EXIST')

	context = {
		'errors':errors,
		'messages':messages,
		'go_back_link':'http://'+get_current_site(request).domain+reverse('specific-class-stream', kwargs={'class_id':urlsafe_base64_encode(force_bytes(specific_lecture_info[2]))})
	}

	return render(request, 'learner_management/confirmation.html', context)


@login_required
def add_lesson_file_view(request, lesson_id):
	try:
		decoded_lesson_id = force_bytes(urlsafe_base64_decode(lesson_id))
		specific_lesson = Lesson.objects.get(pk=decoded_lesson_id)
	except(TypeError, ValueError, OverflowError, Lesson.DoesNotExist):
		specific_lesson = None
	form = AddLessonFileForm()
	existing_lesson_files = []
	errors = []
	if specific_lesson is not None:
		existing_files = specific_lesson.lessonfile.all()
		combined_file_size = byte_to_mb(sum([existing_file.file.size for existing_file in existing_files]))
		if specific_lesson.lesson_class.instructor == request.user:
			form = AddLessonFileForm(request.POST, request.FILES)

			if request.method == 'POST':
				if form.is_valid():
					file_name = form.cleaned_data.get('file').name
					# check if the file being uploaded is already on the list of existing files
					if not check_duplicate_file(existing_files, form.cleaned_data.get('file')):
						file_size = byte_to_mb(form.cleaned_data.get('file').size)
						# check whether if the uploaded file will exceed the combined file size when they are added
						if file_size + combined_file_size < byte_to_mb(settings.MAX_COMBINED_FILE_SIZE):
							a = form.save(commit=False)
							a.lesson = specific_lesson
							a.save()
						else:
							errors.append(f'You exceeded the combined file size limit of {byte_to_mb(settings.MAX_COMBINED_FILE_SIZE)}mb, current combined size {combined_file_size}mb, you are trying to upload a file of size {file_size}mb')
					else:
						errors.append(f'The file {file_name} is already uploaded')
		else:
			return redirect('home')
	else:
		return redirect('home')

	if specific_lesson is not None:
		# get all the existing lesson files 
		#LessonFile.objects.filter(lesson=specific_lesson)
		for existing_file in specific_lesson.lessonfile.all():
			delete_link = 'http://'+get_current_site(request).domain+reverse('delete-lesson-file', kwargs={'lesson_file_id':urlsafe_base64_encode(force_bytes(existing_file.id)), 'lesson_id':lesson_id})
			efi = (existing_file.file.name, existing_file.file.url, delete_link, existing_file.file.size)
			existing_lesson_files.append(efi)

	context = {
		'form':form,
		'title':specific_lesson.title,
		'lesson_files_info':existing_lesson_files,
		'lesson_link': 'http://'+get_current_site(request).domain+reverse('specific-lesson', kwargs={'lesson_id':lesson_id}),
		'total_file_size': combined_file_size,
		'errors':errors
	}

	return render(request, 'learner_management/add_lesson_file.html', context)

@login_required
def specific_lesson_view(request, lesson_id):
	try:
		decoded_lesson_id = force_bytes(urlsafe_base64_decode(lesson_id))
		specific_lesson = Lesson.objects.get(pk=decoded_lesson_id)
	except(ValueError, TypeError, OverflowError, Lesson.DoesNotExist):
		specific_lesson = None

	lesson_files_info = []
	if specific_lesson is not None:
		# check if the user is a student of the class that has lesson or the instructor of the class
		if request.user in specific_lesson.lesson_class.students.all() or request.user == specific_lesson.lesson_class.instructor:
			lesson_files = specific_lesson.lessonfile.all() #LessonFile.objects.filter(lesson=specific_lesson)
			# get the name of the file and there link
			for lesson_file in lesson_files:
				lfi = (lesson_file.file.name, lesson_file.file.url)
				lesson_files_info.append(lfi)
			add_lesson_file_link = 'http://'+get_current_site(request).domain + reverse('add-lesson-file', kwargs={'lesson_id':lesson_id})

			# if the user is the instructor the student link should not be generated
			is_class_instructor = False
			student_work_link = '#'
			student_works_links = []
			if not request.user == specific_lesson.lesson_class.instructor:
				student_work = StudentWork.objects.get(student=request.user, lesson=specific_lesson)
				student_work_link = 'http://'+get_current_site(request).domain + reverse('student-work-file', kwargs={'student_work_id':urlsafe_base64_encode(force_bytes(student_work.pk))})	
				is_class_instructor = True	
			else:
				for student_work in specific_lesson.studentwork.all():
					link = 'http://'+get_current_site(request).domain + reverse('student-work-file', kwargs={'student_work_id':urlsafe_base64_encode(force_bytes(student_work.pk))})
					student_name = student_work.student.profile.first_name + " " + student_work.student.profile.last_name
					status=''
					if student_work.turned_in:
						status = 'Turned in'
					else:
						status = 'Assisgned'
					student_works_links.append((student_name, link, status, student_work.late))
		else:
			return redirect('home')
	else:
		return redirect('home')

	context = {
		'lesson':specific_lesson,
		'lesson_files_info':lesson_files_info,
		'add_lesson_file_link':add_lesson_file_link,
		'deadline_date':specific_lesson.deadline,
		'student_work_link':student_work_link,
		'is_class_instructor':is_class_instructor,
		'student_works_links':student_works_links,
		'instructor_name': specific_lesson.lesson_class.instructor.profile.first_name + ' ' + specific_lesson.lesson_class.instructor.profile.last_name,
		'go_back_link': 'http://'+get_current_site(request).domain + reverse('specific-class-stream', kwargs={'class_id':urlsafe_base64_encode(force_bytes(specific_lesson.lesson_class.pk))}),
		'edit_lesson_link':'http://'+get_current_site(request).domain + reverse('edit-lesson', kwargs={'lesson_id':lesson_id}),
		'delete_lesson_link':'http://'+get_current_site(request).domain + reverse('delete-lesson', kwargs={'lesson_id':lesson_id})
	}
	return render(request, 'learner_management/specific_lesson.html', context)

@login_required
def specific_lecture_view(request, lecture_id):
	try:
		decoded_lecture_id = force_bytes(urlsafe_base64_decode(lecture_id))
		specific_lecture = Lecture.objects.get(pk=decoded_lecture_id)
	except(ValueError, TypeError, OverflowError, Lecture.DoesNotExist):
		specific_lecture = None

	lecture_files_info = []
	commentForm = LectureCommentForm()
	if specific_lecture is not None:
		# check if the user is a student of the class that has lesson or the instructor of the class
		if request.user in specific_lecture.lecture_class.students.all() or request.user == specific_lecture.lecture_class.instructor:
			lecture_files = specific_lecture.lecturefile.all() #LessonFile.objects.filter(lesson=specific_lesson)
			# get the name of the file and there link
			for lecture_file in lecture_files:
				lfi = (lecture_file.file.name, lecture_file.file.url)
				lecture_files_info.append(lfi)
			add_lecture_file_link = 'http://'+get_current_site(request).domain + reverse('add-lecture-file', kwargs={'lecture_id':lecture_id})

			if request.method == 'POST':
				commentForm = LectureCommentForm(request.POST)
				# check to see if the user is a stuednt or a teacher to sub,it a comment
				if commentForm.is_valid():
					comment = commentForm.save(commit=False)
					comment.lecture = specific_lecture
					comment.author = request.user
					comment.save()
					commentForm = LectureCommentForm()
			# get all the comment info
			comment_info = []
			for comment in specific_lecture.lecturecomment.all():
				comment_author_name = comment.author.profile.get_fullname()
				comment_author_profile_pic = comment.author.profile.profile_pic.url
				comment_info.append((comment_author_name, comment.content, comment.timestamp, comment_author_profile_pic))

		else:
			return redirect('home')
	else:
		return redirect('home')

	context = {
		'commentform':commentForm,
		'comment_info':comment_info,
		'lecture':specific_lecture,
		'lecture_files_info':lecture_files_info,
		'add_lecture_file_link':add_lecture_file_link,
		'is_class_instructor':request.user == specific_lecture.lecture_class.instructor,
		'instructor_name': specific_lecture.lecture_class.instructor.profile.get_fullname(),
		'go_back_link': 'http://'+get_current_site(request).domain + reverse('specific-class-stream', kwargs={'class_id':urlsafe_base64_encode(force_bytes(specific_lecture.lecture_class.pk))}),
		'edit_lecture_link':'http://'+get_current_site(request).domain + reverse('edit-lecture', kwargs={'lecture_id':lecture_id}),
		'delete_lecture_link':'http://'+get_current_site(request).domain + reverse('delete-lecture', kwargs={'lecture_id':lecture_id})
	}
	return render(request, 'learner_management/specific_lecture.html', context)

@login_required
def delete_lesson_file_view(request, lesson_file_id, lesson_id):
	try:
		decoded_lesson_file_id = force_bytes(urlsafe_base64_decode(lesson_file_id))
		specific_lesson_file = LessonFile.objects.get(pk=decoded_lesson_file_id)
	except(TypeError, ValueError, OverflowError, LessonFile.DoesNotExist):
		specific_lesson_file = None;

	if specific_lesson_file is not None:
		if specific_lesson_file.lesson.lesson_class.instructor == request.user:
			specific_lesson_file.delete()
			return redirect('add-lesson-file', lesson_id=lesson_id)
	# return redirect('add-lesson-file', lesson_id = lesson_id)
	return redirect('home')


@login_required
def delete_lecture_file_view(request, lecture_file_id, lecture_id):
	try:
		decoded_lecture_file_id = force_bytes(urlsafe_base64_decode(lecture_file_id))
		specific_lecture_file = LectureFile.objects.get(pk=decoded_lecture_file_id)
	except(TypeError, ValueError, OverflowError, LectureFile.DoesNotExist):
		specific_lecture_file = None;

	if specific_lecture_file is not None:
		if specific_lecture_file.lecture.lecture_class.instructor == request.user:
			specific_lecture_file.delete()
			return redirect('add-lecture-file', lecture_id=lecture_id)
	# return redirect('add-lesson-file', lesson_id = lesson_id)
	return redirect('home')

def get_lesson_view(request):
	return render(request, 'learner_management/get_lesson.html', {'domain':get_current_site(request).domain})


@login_required
def lecture_comment_view(request, lecture_id):
	try:
		decoded_lecture_id = force_bytes(urlsafe_base64_decode(lecture_id))
		specific_lecture = Lecture.objects.get(pk=decoded_lecture_id)

	except(TypeError, ValueError, OverflowError, Lecture.DoesNotExist):
		student_work = None

	commentForm = LectureCommentForm()
	message = ''
	if specific_lecture is not None:
		domain = 'http://'+get_current_site(request).domain
		if request.method == 'POST':
			commentForm = LectureCommentForm(request.POST)

			# check to see if the user is a stuednt or a teacher to sub,it a comment
			if commentForm.is_valid() and (LMSClass.objects.students.all().get(students=request.user).exists() or request.user == lecture.lecture_class.instructor):
				comment = commentForm.save(commit=False)
				comment.lecture = specific_lecture
				comment.author = request.user
				comment.save()
				commentForm = LectureCommentForm()

				message = 'Comment form is submitted'
			
			
	else:
		return redirect('myclasses_view')
	comment_info = []


	for comment in specific_lecture.lecturecomment.all():
		comment_author_name = comment.author.get_fullname()
		comment_author_profile_pic = comment.author.profile.profile_pic.url
		comment_info.append((comment_author_name, comment.content, comment.timestamp, comment_author_profile_pic))

	context={
		'commentform':commentForm,
		'message':message,
		'comment_info':comment_info,
		'is_instructor':request.user == lecture.lecture_class.instructor
	}
	return render(request, 'learner_management/lecture_comment.html', context)
