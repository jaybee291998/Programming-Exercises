from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

class Admin(models.Model):
	model_name 			= models.CharField(max_length=255, default='default mode name')
	admins 				= models.ManyToManyField(User, related_name='admins')
	pending_instructors = models.ManyToManyField(User, related_name='my_instructor_request')

	def __str__(self):
		return self.model_name

class Announcement(models.Model):
	title 			= models.CharField(max_length=255)
	description 	= models.TextField()
	timestamp 		= models.DateTimeField(auto_now_add=True)
	author			= models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_announcements')

	def __str__(self):
		return self.title


class AnnouncementImage(models.Model):
	announcement 	= models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='announcementimages')
	image 			= models.ImageField()

	def __str__(self):
		return self.announcement.title

	# def delete(self, using=None, keep_parents=False):
	# 	storage = self.image.storage

	# 	if storage.exists(self.image.name):
	# 		storage.delete(self.image.name)

	# 	super().delete()
