from django import forms 
from .models import Announcement, AnnouncementImage

class AnnouncementForm(forms.ModelForm):
	title 			= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Title', 'class':'form-control'}))
	description 	= forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Description', 'class':'form-control'}))


	class Meta:
		model = Announcement
		fields = [
			'title',
			'description',
		]

class AnnouncementImageForm(forms.ModelForm):

	# name		= forms.CharField()
	image 		= forms.ImageField()

	class Meta:
		model = AnnouncementImage
		fields = [
			'image'
		]

class EditAnnouncementForm(forms.ModelForm):
	title 			= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Title', 'class':'form-control'}))
	description 	= forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Description', 'class':'form-control'}))


	class Meta:
		model = Announcement
		fields = [
			'title',
			'description'
		]