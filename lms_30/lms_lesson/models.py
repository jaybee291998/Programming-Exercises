from django.db import models
from django.db.models.signals import post_delete,pre_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
User = get_user_model()
# Create your models here.

from django.db.models import FileField
from django import forms 

# other model dependencies
from lms_class.models import LMSClass

from lms.utils import mb_to_bytes, byte_to_mb

class Lesson(models.Model):
	title			= models.CharField(max_length=255)
	description		= models.TextField()

	# type of lesson
	class TypeOfLesson(models.TextChoices):
		# LECTURE 		= 'LC', _('Lecture')
		QUIZ 			= 'QZ', _('Quiz')
		ASSISGNMENT 	= 'AS', _('Assignment')
		ACTIVITY 		= 'AC', _('Activity')
		EXAM	 		= 'EX', _('Exam')

	# term
	class Term(models.TextChoices):
		PRELIM			= 'PRE',_('Prelim')
		MIDTERM			= 'MID',_('Midterm')
		SEMI			= 'SEM',_('Semi-finals')
		FIN 			= 'FIN',_('Finals')

	type_of_lesson	= models.CharField(
		max_length=2,
		choices=TypeOfLesson.choices,
		default=TypeOfLesson.QUIZ
	)

	term = models.CharField(
		max_length=3,
		choices=Term.choices,
		default=Term.PRELIM
	)

	lesson_class 	= models.ForeignKey(LMSClass, on_delete=models.CASCADE, related_name='lesson', null=True)
	total_mark		= models.IntegerField(default=100)
	timestamp		= models.DateTimeField(auto_now_add=True)
	deadline		= models.DateTimeField()
	num				= models.IntegerField(default=0)

	def __str__(self):
		return self.title

	def get_type():
		return 'lesson'

class Lecture(models.Model):
	title			= models.CharField(max_length=255)
	description		= models.TextField()
	lecture_class 	= models.ForeignKey(LMSClass, on_delete=models.CASCADE, related_name='lecture', null=True)
	timestamp		= models.DateTimeField(auto_now_add=True)
	

	type_of_lecture		= models.CharField(max_length=32)

	def __str__(self):
		return self.type_of_lecture + ': ' + self.title

	def get_type():
		return 'lecture'

class CustomFileField(FileField):
    def __init__(self, content_types=None, max_upload_size=None, *args, **kwargs):
        self.content_types = content_types
        self.max_upload_size = max_upload_size

        super(CustomFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):        
        data = super(CustomFileField, self).clean(*args, **kwargs)
        
        file = data.file
        try:
            if file.size > self.max_upload_size:
                raise forms.ValidationError(f'Please keep the file size under {byte_to_mb(self.max_upload_size)}mb, current size {byte_to_mb(file.size)}mb')
        except AttributeError:
            pass        
            
        return data


class LessonFile(models.Model):
	file 					= CustomFileField(
								content_types=['application/pdf', 'application/zip'],
								max_upload_size=mb_to_bytes(5)
								)
	lesson 					= models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lessonfile', null=True)

	def __str__(self):
		return self.file.name

	def delete(self, using=None, keep_parent=False):
		storage = self.file.storage

		if storage.exists(self.file.name):
			storage.delete(self.file.name)

		super().delete()

class LectureFile(models.Model):
	file 					= CustomFileField(
								content_types=['application/pdf', 'application/zip'],
        						max_upload_size=mb_to_bytes(5)
								)
	lecture 				= models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='lecturefile')

	def __str__(self):
		return self.file.name
		
	# def delete(self, using=None, keep_parent=False):
	# 	storage = self.file.storage

	# 	if storage.exists(self.file.name):
	# 		storage.delete(self.file.name)

	# 	super().delete()

	# """ Whenever ANY model is deleted, if it has a file field on it, delete the associated file too"""
	# @receiver(post_delete)
	# def delete_files_when_row_deleted_from_db(sender, instance, **kwargs):
	#     for field in sender._meta.concrete_fields:
	#         if isinstance(field,models.FileField):
	#             instance_file_field = getattr(instance,field.name)
	#             delete_file_if_unused(sender,instance,field,instance_file_field)
	            
	# """ Delete the file if something else get uploaded in its place"""
	# @receiver(pre_save)
	# def delete_files_when_file_changed(sender,instance, **kwargs):
	#     # Don't run on initial save
	#     if not instance.pk:
	#         return
	#     for field in sender._meta.concrete_fields:
	#         if isinstance(field,models.FileField):
	#             #its got a file field. Let's see if it changed
	#             try:
	#                 instance_in_db = sender.objects.get(pk=instance.pk)
	#             except sender.DoesNotExist:
	#                 # We are probably in a transaction and the PK is just temporary
	#                 # Don't worry about deleting attachments if they aren't actually saved yet.
	#                 return
	#             instance_in_db_file_field = getattr(instance_in_db,field.name)
	#             instance_file_field = getattr(instance,field.name)
	#             if instance_in_db_file_field.name != instance_file_field.name:
	#                 delete_file_if_unused(sender,instance,field,instance_in_db_file_field)

	# """ Only delete the file if no other instances of that model are using it"""    
	# def delete_file_if_unused(model,instance,field,instance_file_field):
	#     dynamic_field = {}
	#     dynamic_field[field.name] = instance_file_field.name
	#     other_refs_exist = model.objects.filter(**dynamic_field).exclude(pk=instance.pk).exists()
	#     if not other_refs_exist:
	#         instance_file_field.delete(False)

class LectureComment(models.Model):
	lecture 		= models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='lecturecomment')
	author 			= models.ForeignKey(User, related_name='lecturecomment', on_delete=models.CASCADE)											#models.CharField(max_length=255)
	content			= models.TextField()
	timestamp		= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.author.profile.get_fullname() + ' - ' + self.lecture.title