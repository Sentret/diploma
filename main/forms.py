from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

from .models import Comment
from .models import Profile
from .models import Event


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class RegistrationForm(forms.ModelForm):
    
    error_messages = {
        'password_missmatch': 'Пароли не совпадают',
        'password_too_short': 'Пароль должен иметь не меньше 8 символов',
        'user_exists': 'Пользователь с таким именем уже существует'
    }


    password1 = forms.CharField()
    password2 = forms.CharField()


    class Meta:
        model = User
        fields = ("username",)
        

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError(self.error_messages['user_exists'])
        return username


    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        length = len(password1)

        if (length < 8):
            raise ValidationError(self.error_messages['password_too_short'])

        return password1


    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError(self.error_messages['password_missmatch'])

        return password2


    def save(self, commit = True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user

    
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()



