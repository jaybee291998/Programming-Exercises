from django import forms 
from .models import LMSClass, LMSClassInfo
from django.contrib.auth import get_user_model
User = get_user_model()

class LMSClassForm(forms.ModelForm):

	name 				= forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder':'Nama', 'class':'form-control'}))
	description			= forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Description', 'class':'form-control'}))

	class Meta:
		model = LMSClass
		fields = [
			'name',
			'description',
			'course',
			'year',
			'semester'
		]

	# def clean(self, *args, **kwargs):
	# 	name 		= self.cleaned_data.get('class_name')
	# 	description	= self.cleaned_data.get('class_description')
class StudentInviteForm(forms.Form):
	email			= forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email', 'class':'form-control'}))
	message			= forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Description', 'class':'form-control'}))

	def clean(self, *args, **kwargs):
		email 		= self.cleaned_data.get('email')
		message		= self.cleaned_data.get('message')
		if not User.objects.filter(email=self.cleaned_data.get('email')).exists():
			raise forms.ValidationError('This email is not registered')

		return super(StudentInviteForm, self).clean(*args, **kwargs)

class DeleteClassForm(forms.Form):
	password 		= forms.CharField(label='Password', widget=forms.PasswordInput)

class UpdateClassBannerForm(forms.ModelForm):
	class Meta:
		model = LMSClassInfo
		fields = ['banner_bg']