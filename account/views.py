from django.shortcuts import render

from main.models import Event
from main.models import EventSubscription


def subscriptions(request):
    events = Event.event_manager.get_subscriptions(request.user)
    return render(request, "account/account.html", {'events':events})


def created_by_user_events(request):
	events = Event.objects.filter(creater=request.user)
	return render(request, "account/account.html", {"events":events})


