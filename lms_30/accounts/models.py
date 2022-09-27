from django.db import models
from django.contrib.auth.models import(
	AbstractBaseUser,
	BaseUserManager
	)
# Create your models here.

class UserManager(BaseUserManager):
	
	def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False, is_confirmed=False):
		if not email:
			raise ValueError("Users must have an email address")
		if not password:
			raise ValueError("Users must have a password")

		user_obj = self.model(
			email = self.normalize_email(email)
			)

		user_obj.set_password(password)
		user_obj.is_staff = is_staff
		user_obj.is_active = is_active
		user_obj.is_admin = is_admin
		user_obj.is_confirmed = is_confirmed
		user_obj.save(using=self._db)

	def create_staffuser(self, email, password=None):
		user = self.create_user(
			email = email,
			password = password,
			is_staff = True
			)
		return user

	def create_superuser(self, email, password=None):
		user = self.create_user(
			email = email,
			password = password,
			is_staff = True,
			is_admin = True,
			is_confirmed = True
			)
		return user


class User(AbstractBaseUser):
	email 		= models.EmailField(max_length=255, unique=True)
	is_active		= models.BooleanField(default=True)
	is_staff		= models.BooleanField(default=False)
	is_admin		= models.BooleanField(default=False)
	is_confirmed	= models.BooleanField(default=False)
	timestamp	= models.DateTimeField(auto_now_add=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELD = []

	objects = UserManager()

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

	def get_full_name(self):
		return self.email

	def get_short_name(self):
		return self.email

class Profile(models.Model):

	COURSES = (
		('BSCS', 'BSCS'),
		('BSED', 'BSED'),
		('BAPS', 'BSPS'))

	YEARS = (
		('1', '1st'),
		('2', '2nd'),
		('3', '3rd'),
		('4', '4th'),
		('5', 'Grad'))
	user 			= models.OneToOneField(User, related_name = 'profile', on_delete=models.CASCADE)
	first_name 		= models.CharField(max_length=255,default="")
	last_name 		= models.CharField(max_length=255, default="")
	profile_pic 	= models.ImageField(blank=True, default="profile_pic.png")
	is_instructor 	= models.BooleanField(default = False)
	course 			= models.CharField(max_length=4, choices=COURSES)
	year 			= models.CharField(max_length=1, choices=YEARS)

	def __str__(self):
		return self.first_name + " " + self.last_name

	def get_fullname(self):
		return self.first_name + ' ' + self.last_name

	
	
	
	
