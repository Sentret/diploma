import json
import datetime

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.contrib import auth
from django.shortcuts import redirect
from django.views import View
from django.db import IntegrityError

from .models import Event
from .models import Location
from .models import EventSubscription


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        #проверяем что пользователь не NONE
        if user:
            auth.login(request, user)
            return redirect('/')
        else:
            return HttpResponse("Неверный логин или пароль")                        
    else:       
        return render(request,'main/login_form.html')


def registration(request):
    pass



def main_page_view(request):
    events = Event.objects.all()
    return render(request,"main/main_page.html",{'events':events})


def event_page(request, id):
    event = get_object_or_404(Event,pk=id)
    subscription = EventSubscription.objects.all().filter(subscriber=request.user, event=event)

    # статус подписка на событие
    subscribed = False
    if(subscription.count() == 1):
        subscribed = True

    return render(request, 'main/event_page.html',{'event':event, 'subscribed':subscribed})


class EventPublish(LoginRequiredMixin, View):

    def get(self, request):
        return render(request,"main/event_form.html")


    def post(self, request):
        event = request.POST

        try:
            lat = float(event['lat'])
            lng = float(event['lng'])
        except:
            lat = 0
            lng = 0

        date = event['date']
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()

        preview = request.FILES.get('preview')
        location = Location.objects.create(lat=lat, lng=lng)
        event = Event.objects.create(location=location, creater=request.user, description=event['description'],
                                        title=event['title'],preview=preview,date=date)
        
        events = Event.objects.all()
        return render(request,"main/main_page.html",{'events':events})

   
class EventSubscriptionView(LoginRequiredMixin, View):
    # подписка и отписка от события
    def post(self,request):
        data = json.loads(request.body)
        event = get_object_or_404(Event, pk=data['event'])

        # подписка
        if (not data['subscribed']):
            subscription = EventSubscription.objects.create(subscriber=request.user, event=event )
           
        #отписка    
        else:
            subscription = EventSubscription.objects.all().filter(subscriber=request.user, event=event )
            subscription.delete()

        return HttpResponse(status=200)









