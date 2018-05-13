from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from main.models import BaseEvent
from main.models import Event
from main.models import Trip
from main.models import Profile
from main.models import EventSubscription
from main.models import Message
from .forms import ProfileForm
from .forms import UserForm

@login_required
def subscriptions(request):
    events = BaseEvent.event_manager.get_subscriptions(request.user)
    return render(request, "account/account.html", {'events':events})


@login_required
def events(request):
	events = Event.objects.filter(creater=request.user)
	return render(request, "account/account.html", {"events":events})


@login_required
def trips(request):
	events = Trip.objects.filter(creater=request.user)
	return render(request, "account/account.html", {"events":events})


class EditProfileView(LoginRequiredMixin, View):
	def get(self, request):
		return render(request, "account/profile_edit.html")

	def post(self, request):
		form = ProfileForm(data=request.POST, files=request.FILES, instance=request.user.profile)
		user_form = UserForm(request.POST, instance=request.user)


		if form.is_valid() and user_form.is_valid():
			form.save()
			user_form.save()
		
		return redirect('edit-profile')


class ProfileView(View):
	def get(self, request, username):
		profile = Profile.objects.get(user__username=username)
		return render(request, 'account/profile_page.html',{'profile':profile})


@login_required
def messages(request):
	messages = Message.objects.filter(recipient=request.user).values('addresser').distinct()
	rooms = []

	for message in messages:
		addresser = User.objects.get(id=message['addresser'])
		room_name =request.user.id * addresser.id
		rooms.append({'addresser':addresser, 'room_name': room_name})		


	context = {
				'rooms':rooms,
			  }
	return render(request, "account/messages.html", context)