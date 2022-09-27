from django import forms 
from .models import LessonFile, Lesson, LessonFile, Lecture, LectureFile, LectureComment

class DateTimeInput(forms.DateTimeInput):
	input_type='datetime-local'

class LessonFileForm(forms.ModelForm):

	# name		= forms.CharField()
	file 		= forms.FileField()

	class Meta:
		model = LessonFile
		fields = [
			'file'
		]

class AddNewLessonForm(forms.ModelForm):
	title 			= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Title', 'class':'form-control'}))
	description 	= forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Instructions', 'class':'form-control'}))
	deadline		= forms.DateTimeField(widget=DateTimeInput)
	total_mark 		= forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'mark', 'class':'form-control'}))
	# num				= forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'quiz num', 'class':'form-control'}))


	class Meta:
		model = Lesson
		fields = [
			'title',
			'description',
			'total_mark',
			'term',
			'type_of_lesson',
			'deadline'
			# 'num'
			
		]

class AddLectureForm(forms.ModelForm):
	title 			= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Title', 'class':'form-control'}))
	description 	= forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Instructions', 'class':'form-control'}))

	class Meta:
		model = Lecture
		fields = [
			'title',
			'description'
		]

class EditLessonForm(forms.ModelForm):
	title 			= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Title', 'class':'form-control'}))
	description 	= forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Instructions', 'class':'form-control'}))
	# deadline		= forms.DateTimeField(widget=DateTimeInput)
	total_mark 		= forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'mark', 'class':'form-control'}))
	num				= forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'quiz num', 'class':'form-control'}))


	class Meta:
		model = Lesson
		fields = [
			'title',
			'description',
			'total_mark',
			'term',
			'type_of_lesson',
			# 'deadline',
			'num'
		]

class EditLectureForm(forms.ModelForm):
	title 			= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Title', 'class':'form-control'}))
	description 	= forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Instructions', 'class':'form-control'}))


	class Meta:
		model = Lesson
		fields = [
			'title',
			'description'
		]

class AddLessonFileForm(forms.ModelForm):
	# file_description		= forms.CharField()
	file 					= forms.FileField()

	class Meta:
		model = LessonFile
		fields = [
			'file'
		]

class AddLectureFileForm(forms.ModelForm):
	# file_description		= forms.CharField()
	file 					= forms.FileField()

	class Meta:
		model = LectureFile
		fields = [
			'file'
		]

class LectureCommentForm(forms.ModelForm):
	content		= forms.CharField(widget=forms.Textarea(attrs={'placeholder':'comment', 'class':'form-control'}))

	class Meta:
		model = LectureComment
		fields = [
			'content'
		]