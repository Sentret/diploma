from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Comment
from .models import Profile


class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ['content']


class RegistrationForm(UserCreationForm):
	
	class Meta:
		model = User
		fields = ("username", "password1", "password2", )

	def save(self, commit = True):
		user = super(RegistrationForm, self).save(commit = True)
		return user