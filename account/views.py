from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from main.models import BaseEvent
from main.models import Profile
from main.models import EventSubscription
from .forms import ProfileForm
from .forms import UserForm


@login_required
def subscriptions(request):
    events = BaseEvent.event_manager.get_subscriptions(request.user)
    return render(request, "account/account.html", {'events':events})

@login_required
def events(request):
	events = BaseEvent.objects.filter(creater=request.user)
	return render(request, "account/account.html", {"events":events})

@login_required
def trips(request):
	events = BaseEvent.objects.filter(creater=request.user)
	return render(request, "account/account.html", {"events":events})


class EditProfileView(LoginRequiredMixin, View):
	def get(self, request):
		return render(request, "account/profile_edit.html")

	def post(self, request):
		form = ProfileForm(data=request.POST, files=request.FILES, instance=request.user.profile)
		user_form = UserForm(request.POST, instance=request.user)

		print(request.POST['last_name'])

		if form.is_valid() and user_form.is_valid():
			form.save()
			user_form.save()
		
		return redirect('edit-profile')


class ProfileView(View):
	def get(self, request, username):
		profile = Profile.objects.get(user__username=username)
		return render(request, 'account/profile_page.html',{'profile':profile})
