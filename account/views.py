from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from main.models import BaseEvent
from main.models import EventSubscription


def subscriptions(request):
    events = BaseEvent.event_manager.get_subscriptions(request.user)
    return render(request, "account/account.html", {'events':events})


def events(request):
	events = BaseEvent.objects.filter(creater=request.user)
	return render(request, "account/account.html", {"events":events})

def trips(request):
	events = BaseEvent.objects.filter(creater=request.user)
	return render(request, "account/account.html", {"events":events})



class EditProfileView(LoginRequiredMixin, View):
	def get(self, request):
		return render(request, "account/profile_edit.html", {"events":events})

	def post(self, request):
		pass
