from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from django.views.generic import TemplateView

from django.contrib.auth import get_user_model
# the user model
User = get_user_model()

#stuffs needed for email
from django.core.mail import EmailMessage
from django.conf import settings

# forms
from .forms import StudentWorkFileForm, StudentWorkCommentForm, StudentWorkMarkForm
from .models import StudentWork, StudentWorkFile, StudentWorkComment
from lms_lesson.models import byte_to_mb


from lms.utils import check_duplicate_file, byte_to_mb

# send emails asynch
from lms.task import send_email_task
# Create your views here.
template_dir = 'lmsstudentwork/'


def _get_form(request, formcls, prefix, instance = None):
	data = ''
	if prefix in request.POST:
		if prefix == 'fileform_pre':
			return formcls(request.POST, request.FILES, prefix=prefix)
		elif prefix == 'markform_pre':
			return formcls(request.POST, instance=instance, prefix=prefix)
		else: 
			return formcls(request.POST, prefix=prefix)
	else:
		return formcls(None, prefix=prefix)


# @login_required
# def student_work_view(request, student_work_id):
# 	try:
# 		decoded_student_work_id = force_bytes(urlsafe_base64_decode(student_work_id))
# 		student_work = StudentWork.objects.get(pk=decoded_student_work_id)

# 	except(TypeError, ValueError, OverflowError, StudentWork.DoesNotExist):
# 		student_work = None

# 	fileForm = StudentWorkFileForm()
# 	commentForm = StudentWorkCommentForm()
# 	markForm = StudentWorkMarkForm()
# 	message = ''
# 	if student_work is not None:
# 		if request.method == 'POST':
# 			fileForm = _get_form(request, StudentWorkFileForm, 'fileform_pre')
# 			commentForm = _get_form(request, StudentWorkCommentForm, 'commentform_pre')
# 			markForm = _get_form(request, StudentWorkMarkForm, 'markform_pre', instance=student_work)
# 			# check to see if the form is bound and the user is the student for this student work to upload a file
# 			if fileForm.is_bound and fileForm.is_valid() and request.user == student_work.student:
# 				file = fileForm.save(commit=False)
# 				file.student_work = student_work
# 				file.save()
# 				# if a student pass the first file, it automatically means the work is submitted
# 				if not student_work.turned_in:
# 					student_work.turned_in = True
# 					student_work.save()
# 					fileForm = StudentWorkFileForm()

# 				message = 'File Form is submitted'
# 			# check to see if the user is a stuednt or a teacher to sub,it a comment
# 			elif commentForm.is_bound and commentForm.is_valid() and (request.user == student_work.student or request.user == student_work.lesson.lesson_class.instructor):
# 				comment = commentForm.save(commit=False)
# 				comment.student_work = student_work
# 				comment.author = request.user;
# 				comment.save()
# 				commentForm = StudentWorkCommentForm()

# 				message = 'Comment form is submitted'

# 			elif markForm.is_bound and markForm.is_valid() and request.user == student_work.lesson.lesson_class.instructor:
# 				markForm.save()
# 				student_work.save()
# 				message = 'Mark Form submitted'
# 				if not student_work.graded:
# 					student_work.graded = True
# 					student_work.save()
# 					markForm = StudentWorkMarkForm()
			
			
# 	else:
# 		return redirect('myclasses_view')

# 	file_info = []
# 	comment_info = []

# 	for file in student_work.studentworkfile.all():
# 		delete_link = 'http://'+get_current_site(request).domain+reverse('delete-student-file', kwargs={'student_file_id':urlsafe_base64_encode(force_bytes(file.id)), 'student_work_id':student_work_id})
# 		file_info.append((file.file.name, file.file.url, file.timestamp, delete_link))

# 	for comment in student_work.studentworkcomment.all():
# 		comment_author_name = comment.author.profile.first_name + ' ' + comment.author.profile.last_name
# 		comment_author_profile_pic = comment.author.profile.profile_pic.url
# 		comment_info.append((comment_author_name, comment.content, comment.timestamp, comment_author_profile_pic))

# 	context={
# 		'fileform':fileForm,
# 		'commentform':commentForm,
# 		'markform':markForm,
# 		'message':message,
# 		'file_info':file_info,
# 		'comment_info':comment_info,
# 		'is_instructor':request.user == student_work.lesson.lesson_class.instructor,
# 		'graded':student_work.graded,
# 		'late':student_work.late,
# 		'grade':student_work.mark
# 	}
# 	return render(request, template_dir+'student_work.html', context)

@login_required
def student_work_mark_view(request, student_work_id):
	try:
		decoded_student_work_id = force_bytes(urlsafe_base64_decode(student_work_id))
		student_work = StudentWork.objects.get(pk=decoded_student_work_id)

	except(TypeError, ValueError, OverflowError, StudentWork.DoesNotExist):
		student_work = None

	markForm = StudentWorkMarkForm(instance=student_work)
	message = ''
	if student_work is not None and request.user == student_work.lesson.lesson_class.instructor:
		domain = 'http://'+get_current_site(request).domain
		mark_link = domain+reverse('student-work-mark', kwargs={'student_work_id':student_work_id})
		file_link = domain+reverse('student-work-file', kwargs={'student_work_id':student_work_id})
		comment_link = domain+reverse('student-work-comment', kwargs={'student_work_id':student_work_id})

		if request.method == 'POST':
			markForm = StudentWorkMarkForm(request.POST, instance=student_work)

			if markForm.is_valid():
				markForm.save()
				student_work.save()
				message = 'Mark Form submitted'
				if not student_work.graded:
					student_work.graded = True
					student_work.save()

					# send a message to the student that there work is already graded
					email_subject = 'Work Graded'
					body = "Your work for the lesson '{lesson_name}' for the class '{class_name}' has been graded\n\n".format(lesson_name=student_work.lesson.title, class_name=student_work.lesson.lesson_class.name)
					body += "Mark: {mark}\nRemark: {remark}\n".format(mark=student_work.mark, remark=student_work.remark)
					sender_email = settings.EMAIL_HOST_USER
					receiver_email = [student_work.student.email]
					send_email_task.delay(email_subject, body, receiver_email)
					markForm = StudentWorkMarkForm()	
	else:
		return redirect('myclasses_view')

	context={
		'markform':markForm,
		'message':message,
		'is_instructor':request.user == student_work.lesson.lesson_class.instructor,
		'graded':student_work.graded,
		'late':student_work.late,
		'grade':student_work.mark,
		'handed_in':student_work.turned_in,
		'lesson_name':student_work.lesson.title,
		'student_name':student_work.student.profile.first_name+' '+student_work.student.profile.last_name,
		'mark_link':mark_link,
		'file_link':file_link,
		'comment_link':comment_link
	}
	return render(request, template_dir+'student_work_mark.html', context)

@login_required
def student_work_file_view(request, student_work_id):
	try:
		decoded_student_work_id = force_bytes(urlsafe_base64_decode(student_work_id))
		student_work = StudentWork.objects.get(pk=decoded_student_work_id)

	except(TypeError, ValueError, OverflowError, StudentWork.DoesNotExist):
		student_work = None

	fileForm = StudentWorkFileForm()
	message = ''
	errors = []
	if student_work is not None and (request.user == student_work.student or request.user == student_work.lesson.lesson_class.instructor):
		existing_files = student_work.studentworkfile.all()
		combined_file_size = byte_to_mb(sum([existing_file.file.size for existing_file in existing_files]))

		domain = 'http://'+get_current_site(request).domain
		mark_link = domain+reverse('student-work-mark', kwargs={'student_work_id':student_work_id})
		file_link = domain+reverse('student-work-file', kwargs={'student_work_id':student_work_id})
		comment_link = domain+reverse('student-work-comment', kwargs={'student_work_id':student_work_id})
		go_back_link = domain+reverse('specific-lesson', kwargs={'lesson_id':urlsafe_base64_encode(force_bytes(student_work.lesson.id))})
		if request.method == 'POST':
			fileForm = StudentWorkFileForm(request.POST, request.FILES)
			# check to see if the form is bound and the user is the student for this student work to upload a file
			if fileForm.is_valid() and request.user == student_work.student:
				file_size = byte_to_mb(fileForm.cleaned_data.get('file').size)
				# check if the combined file size is less than the max combined file size
				if file_size + combined_file_size < byte_to_mb(settings.MAX_COMBINED_FILE_SIZE):
					file_name = fileForm.cleaned_data.get('file').name
					#check if the file that is uploaded already exist in the existing files
					if not check_duplicate_file(existing_files, fileForm.cleaned_data.get('file')):
						
						file = fileForm.save(commit=False)
						file.student_work = student_work
						file.save()
						# if a student pass the first file, it automatically means the work is submitted
						if not student_work.turned_in:
							student_work.turned_in = True
							student_work.save()
							fileForm = StudentWorkFileForm()

						message = 'File Form is submitted'
					else:
						errors.append(f'The file {file_name} is already uploaded')
				else:
					errors.append(f'You exceeded the combined file size limit of {byte_to_mb(settings.MAX_COMBINED_FILE_SIZE)}mb, current combined size {combined_file_size}mb, you are trying to upload a file of size {file_size}mb')
					print(errors)
	else:
		return redirect('myclasses_view')

	file_info = []

	for file in student_work.studentworkfile.all():
		delete_link = 'http://'+get_current_site(request).domain+reverse('delete-student-file', kwargs={'student_file_id':urlsafe_base64_encode(force_bytes(file.id)), 'student_work_id':student_work_id})
		file_info.append((file.file.name, file.file.url, file.timestamp, delete_link))


	context={
		'fileform':fileForm,
		'message':message,
		'file_info':file_info,
		'is_instructor':request.user == student_work.lesson.lesson_class.instructor,
		'graded':student_work.graded,
		'late':student_work.late,
		'grade':student_work.mark,
		'remark':student_work.remark,
		'mark_link':mark_link,
		'file_link':file_link,
		'comment_link':comment_link,
		'go_back_link':go_back_link,
		'errors':errors,
		'combined_file_size':combined_file_size
	}
	return render(request, template_dir+'student_work_file.html', context)

@login_required
def student_work_comment_view(request, student_work_id):
	try:
		decoded_student_work_id = force_bytes(urlsafe_base64_decode(student_work_id))
		student_work = StudentWork.objects.get(pk=decoded_student_work_id)

	except(TypeError, ValueError, OverflowError, StudentWork.DoesNotExist):
		student_work = None

	commentForm = StudentWorkCommentForm()
	message = ''
	if student_work is not None:
		domain = 'http://'+get_current_site(request).domain
		mark_link = domain+reverse('student-work-mark', kwargs={'student_work_id':student_work_id})
		file_link = domain+reverse('student-work-file', kwargs={'student_work_id':student_work_id})
		comment_link = domain+reverse('student-work-comment', kwargs={'student_work_id':student_work_id})
		if request.method == 'POST':
			commentForm = StudentWorkCommentForm(request.POST)

			# check to see if the user is a stuednt or a teacher to sub,it a comment
			if commentForm.is_valid() and (request.user == student_work.student or request.user == student_work.lesson.lesson_class.instructor):
				comment = commentForm.save(commit=False)
				comment.student_work = student_work
				comment.author = request.user;
				comment.save()
				commentForm = StudentWorkCommentForm()

				message = 'Comment form is submitted'
			
			
	else:
		return redirect('myclasses_view')
	comment_info = []


	for comment in student_work.studentworkcomment.all():
		comment_author_name = comment.author.profile.first_name + ' ' + comment.author.profile.last_name
		comment_author_profile_pic = comment.author.profile.profile_pic.url
		comment_info.append((comment_author_name, comment.content, comment.timestamp, comment_author_profile_pic))

	context={
		'commentform':commentForm,
		'message':message,
		'comment_info':comment_info,
		'is_instructor':request.user == student_work.lesson.lesson_class.instructor,
		'mark_link':mark_link,
		'file_link':file_link,
		'comment_link':comment_link
	}
	return render(request, template_dir+'student_work_comment.html', context)


@login_required
def delete_student_file_view(request, student_file_id, student_work_id):
	try:
		decoded_student_file_id = force_bytes(urlsafe_base64_decode(student_file_id))
		specific_student_file = StudentWorkFile.objects.get(pk=decoded_student_file_id)
	except(TypeError, ValueError, OverflowError, StudentWorkFile.DoesNotExist):
		specific_student_file = None

	if specific_student_file is not None:
		if request.user == specific_student_file.student_work.student:
			specific_student_file.delete()
			return redirect('student-work-file', student_work_id=student_work_id)

	return redirect('home')






