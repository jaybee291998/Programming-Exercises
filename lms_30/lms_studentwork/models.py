from django.db import models

# model dependencies
from django.contrib.auth import get_user_model

User = get_user_model() 

# Create your models here.
from lms_lesson.models import Lesson, Lecture, CustomFileField, mb_to_bytes

class StudentWork(models.Model):
	student 				= models.ForeignKey(User, on_delete=models.CASCADE, related_name='studentwork', null=True)
	lesson 					= models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='studentwork')
	mark					= models.IntegerField(default=-1)
	remark					= models.TextField(default='Good Job :)')
	turned_in				= models.BooleanField(default=False)
	graded					= models.BooleanField(default=False)
	late 					= models.BooleanField(default=False)

	def __str__(self):
		return self.lesson.title + ": " + self.student.profile.first_name


class StudentWorkFile(models.Model):
	student_work 	= models.ForeignKey(StudentWork, on_delete=models.CASCADE, related_name='studentworkfile')
	file 			= CustomFileField(
						content_types=['application/pdf', 'application/zip'],
						max_upload_size=mb_to_bytes(5)
					)
	timestamp		= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.student_work.lesson.title + "-" + self.student_work.student.profile.first_name + " " + self.student_work.student.profile.last_name + ": " + self.file.name

	# def delete(self, using=None, keep_parent=False):
	# 	storage = self.file.storage

	# 	if storage.exists(self.file.name):
	# 		storage.delete(self.file.name)

	# 	super().delete()

class StudentWorkComment(models.Model):
	student_work 	= models.ForeignKey(StudentWork, on_delete=models.CASCADE, related_name='studentworkcomment')
	author 			= models.ForeignKey(User, related_name='studentworkcomment', on_delete=models.CASCADE)											#models.CharField(max_length=255)
	content			= models.TextField()
	timestamp		= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.student_work)+ ": " + self.author.profile.first_name+self.author.profile.last_name
	