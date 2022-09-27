from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Create your models here.

User = get_user_model()

class LMSClass(models.Model):
	# Course
	class Course(models.TextChoices):
		BSCS 		= 'CS',_('BSCS')
		BSED		= 'ED',_('BSED')
		BAPS 		= 'PS',_('BAPS')

	# Year
	class Year(models.TextChoices):
		FIRST 		= '1',_('1st')
		SECOND 		= '2',_('2nd')
		THIRD 		= '3',_('3rd')
		FOURTH		= '4',_('4th')
		GRAD 		= '5',_('Grad')

	# semester
	class Semester(models.TextChoices):
		FIRST_SEM			= 'FS',_('First Sem')
		SECOND_SEM			= 'SS',_('Second Sem')


	name			= models.CharField(max_length=255)
	description		= models.TextField()
	instructor 		= models.ForeignKey(User, related_name='classes_taugth', on_delete=models.CASCADE, null=True)
	class_token		= models.CharField(max_length=255)
	students		= models.ManyToManyField(User, related_name='classes')
	course 			= models.CharField(max_length=2, choices=Course.choices, default=Course.BSCS)
	year 			= models.CharField(max_length=1, choices=Year.choices, default=Year.FIRST)
	semester 		= models.CharField(max_length=2, choices=Semester.choices, default=Semester.FIRST_SEM)
	# a list of students that want to join the class
	pending_students= models.ManyToManyField(User, related_name='pending_class')
	invited_students= models.ManyToManyField(User, related_name='invited_class')

	def __str__(self):
		return self.name


# # a model that keeps track to the number of a specific type of lesson like quizzes for each term
# class TermCounts(models.Model):
# 	pre				= models.IntegerField(default=0)
# 	mid 			= models.IntegerField(default=0)
# 	sem 			= models.IntegerField(default=0)
# 	fin 			= models.IntegerField(default=0)


class LMSClassInfo(models.Model):
	lmsclass 		= models.OneToOneField(LMSClass, related_name='lmsclassinfo', on_delete=models.CASCADE)
	banner_bg		= models.ImageField(blank=True, default='banner2.png')

	def __str__(self):
		return 'info: ' + self.lmsclass.name


