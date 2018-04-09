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

from .models import Location
from .models import EventSubscription
from .models import BaseEvent
from .models import Event
from .models import Trip
from .models import Comment
from .forms  import CommentForm

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
        return render(request,'main/auth/login_form.html')


def registration(request):
    pass


def main_page_view(request):
    events = BaseEvent.objects.all()
    return render(request,"main/main_page.html",{'events':events})


def event_page(request, id):
    event = get_object_or_404(BaseEvent,pk=id)
    subscribed = event.is_user_subscribed(request.user)
    location = Location.objects.filter(event=event)[0]
    comments = Comment.objects.filter(event=event)
    form = CommentForm()

    if(hasattr(event,'event')):
        return render(request, 'main/event_page.html', {'event':event, 'subscribed':subscribed,'location':location, 'comments':comments, 'form':form})

    else:
        locations = Location.objects.filter(event=event)
        return render(request, 'main/trip/trip_page.html', {'trip':event, 'subscribed':subscribed,'locations':locations, 'comments':comments})


def event_delete(request,id):
    event = get_object_or_404(BaseEvent,pk=id)
    event.delete()    
    return redirect('main-page')


class EventEdit(LoginRequiredMixin, View):
    def get(self, request, id):
        event = get_object_or_404(Event, pk=id)
        location = Location.objects.filter(event=event)[0]
        return render(request,"main/event_edit_form.html", {'event':event,'location':location})


    def post(self, request, id):
        data = request.POST
        event = get_object_or_404(Event, pk=id)

        try:
            lat = float(data['lat'])
            lng = float(data['lng'])
        except:
            lat = 0
            lng = 0

  
        date = data['date']
        date = date.replace('T',' ')
        date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M').date()
        
        
        preview = request.FILES.get('preview')
       
        if(preview is not None):
            event.preview = preview

        location = Location.objects.filter(event=event)
        location.delete()
        location = Location.objects.create(lat=lat, lng=lng, address=data['address'], event=event)

        event.description = data['description']
        event.title=data['title']
        event.date = date

        event.save()
        events = Event.objects.all()
        return render(request,"main/main_page.html",{'events':events})    



class EventPublish(LoginRequiredMixin, View):

    def get(self, request):
        return render(request,"main/event_form.html")


    def post(self, request):
        data = request.POST

        try:
            lat = float(event['lat'])
            lng = float(event['lng'])
        except:
            lat = 0
            lng = 0


  
        date = data['date']
        date = date.replace('T',' ')
        date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M').date()
        preview = request.FILES.get('preview')
        
        event = Event.objects.create(creater=request.user, description=data['description'],
                                        title=data['title'],preview=preview,date=date)

        location = Location.objects.create(lat=lat, lng=lng,address=data['address'], event=event)
        events = Event.objects.all()
        return render(request,"main/main_page.html",{'events':events})

   
class EventSubscriptionView(LoginRequiredMixin, View):
    # подписка и отписка от события
    def post(self,request):
        data = json.loads(request.body)
        event = get_object_or_404(BaseEvent, pk=data['event'])

        # подписка
        if (not data['subscribed']):
            event.subscribe(request.user)

        #отписка    
        else:
            event.unsubscribe(request.user)
            
        return HttpResponse(status=200)



# Trips views

class TripPublish(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'main/trip/trip_form.html')

    def post(self, request):
        data = request.POST

        try:
            lat = float(event['lat'])
            lng = float(event['lng'])
        except:
            lat = 0
            lng = 0

          
        date = data['date']
        date = date.replace('T',' ')
        date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M').date()
        preview = request.FILES.get('preview')
        
        event = Trip.objects.create(creater=request.user, description=data['description'],
                                        title=data['title'],preview=preview,date=date)
        

        locations =  json.loads(data['locations'])

        for loc in locations:
            location = Location.objects.create(lat=loc['position'][0], lng=loc['position'][1],address=loc['address'], event=event)
       
        events = BaseEvent.objects.all()
        return render(request,"main/main_page.html",{'events':events})


