from django.shortcuts import render

from main.models import Event
from main.models import EventSubscription

def subscriptions(request):

    subs = EventSubscription.objects.filter(subscriber=request.user)
    return render(request, "account/account.html", {'subscriptions':subs})


def created_event(request):
	events = Event.objects.filter(creater=request.user)
	return render(request, "account/events.html", {"events":events})


