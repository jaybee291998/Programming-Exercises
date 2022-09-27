from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from accounts.models import Profile

User = get_user_model()

class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class UserLoginForm(forms.Form):
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email', 'class':'form-control'}))
	password = forms.CharField(widget = forms.PasswordInput(attrs={'placeholder':'Password', 'class':'form-control'}))

	def clean(self, *args, **kwargs):
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')

		if email and password:
			user = authenticate(email=email, password=password)
			if not User.objects.filter(email=email).exists():
				raise forms.ValidationError("This user does not exist")
			if User.objects.filter(email=email).exists() and not User.objects.get(email=email).is_active:
				
				raise forms.ValidationError("User is not active, please check your spam inbox for the verification link, or you can resend it by following the link below")
			if not user:
				raise forms.ValidationError("Incorrect Password")
		return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):

	email = forms.EmailField(label="Email address", widget=forms.TextInput(attrs={'placeholder':'Email', 'class':'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password', 'class':'form-control'}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password', 'class':'form-control'}))


	class Meta:
		model = User
		fields = [
			'email',
			'password',
			'password2'
		]

	def clean(self, *args, **kwargs):
		email = self.cleaned_data.get('email')
		
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')

		if password != password2:
			raise forms.ValidationError("passwords must match")
		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("This email is already being used")
		return super(UserRegisterForm, self).clean(*args, **kwargs)

class EditProfileForm(forms.ModelForm):
	first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Fist name', 'class':'form-control'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last name', 'class':'form-control'}))
	# course = forms.CharField()
	# year = forms.CharField()
	profile_pic = forms.ImageField()

	class Meta:
		model = Profile
		fields = [
			'first_name',
			'last_name',
			'course',
			'year',
			'profile_pic'
		]

	def clean(self, *args, **kwargs):
		first_name = self.cleaned_data.get('first_name')
		last_name = self.cleaned_data.get('last_name')
		profile_pic = self.cleaned_data.get('profile_pic')

class ResendVerificationForm(forms.Form):
	email 			= forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email', 'class':'form-control'}))
