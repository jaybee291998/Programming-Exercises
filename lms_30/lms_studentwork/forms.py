from django import forms 
from .models import StudentWorkFile, StudentWorkComment, StudentWork


class StudentWorkFileForm(forms.ModelForm):
	file 		= forms.FileField()

	class Meta:
		model = StudentWorkFile
		fields=[
			'file'
		]

class StudentWorkCommentForm(forms.ModelForm):
	content		= forms.CharField(widget=forms.Textarea(attrs={'placeholder':'comment', 'class':'form-control'}))

	class Meta:
		model = StudentWorkComment
		fields = [
			'content'
		]
class StudentWorkMarkForm(forms.ModelForm):
	mark 		= forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'mark', 'class':'form-control'}))
	remark		= forms.CharField(widget=forms.Textarea(attrs={'placeholder':'remark', 'class':'form-control'}))
	class Meta:
		model = StudentWork
		fields=[
			'mark',
			'remark'
		]
