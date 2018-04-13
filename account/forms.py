from django.forms import ModelForm
from django.contrib.auth.models import User

from main.models import Profile


class ProfileForm(ModelForm):
	class Meta:
		model = Profile
		fields = ['avatar','about']

class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ['first_name','last_name']