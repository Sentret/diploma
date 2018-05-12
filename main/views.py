import json
import datetime
from django.http import Http404
from django.http import JsonResponse

from django.shortcuts import render
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import auth
from django.views import View
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Location
from .models import EventSubscription
from .models import BaseEvent
from .models import Event
from .models import Trip
from .models import Comment
from .models import Profile
from .models import BaseEventCategory
from .forms  import CommentForm
from .forms  import RegistrationForm


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


@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')


class RegistrationView(View):
    def get(self, request):
        return render(request,'main/auth/register_form.html')

    def post(self, request):
        form = RegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)        
            auth.login(request, user)
            return redirect('main-page')
        else:
            print(form.errors)
        return render(request,'main/auth/register_form.html',{'form':form})


def main_page_view(request):
    categories = BaseEventCategory.objects.all().order_by('name')
    return render(request,"main/main_page.html",{'categories':categories})


def  event_page(request, id):
    event = get_object_or_404(BaseEvent,pk=id)
    subscribed = event.is_user_subscribed(request.user)
    location = Location.objects.filter(event=event)[0]
    subscriptions = event.get_subscribers()

    if request.method=='POST':
        Comment.objects.create(user=request.user, event=event, content=request.POST['content'])
        return redirect('event_page',id)

    comments = Comment.objects.filter(event=event).order_by('-date')

    if(hasattr(event,'event')):
        return render(request, 'main/event_page.html', {'event':event, 'subscribed':subscribed,'location':location, 'comments':comments, 'subscriptions':subscriptions})

    else:
        locations = Location.objects.filter(event=event)
        return render(request, 'main/trip/trip_page.html', {'trip':event, 'subscribed':subscribed,'locations':locations, 'comments':comments})


@login_required
def event_delete(request,id):
    event = get_object_or_404(BaseEvent,pk=id)

    if(request.user != event.creater):
        return HttpResponse(status=403)

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

        if(request.user != event.creater):
            return HttpResponse(status=403)

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
        categories = BaseEventCategory.objects.all()
        return render(request,"main/event_form.html", {'categories':categories})


    def post(self, request):
        data = request.POST
        
        category = BaseEventCategory.objects.filter(name=data['category'])[0]

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
        
        event = Event.objects.create(creater=request.user, description=data['description'],
                                        title=data['title'],preview=preview,date=date, category=category)

        location = Location.objects.create(lat=lat, lng=lng,address=data['address'], event=event)
        events = Event.objects.all()
        return render(request,"main/main_page.html",{'events':events})

   
class EventSubscriptionView(LoginRequiredMixin, View):
    
    def post(self,request):
        data = json.loads(request.body.decode('utf-8'))
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
        categories = BaseEventCategory.objects.all()
        return render(request, 'main/trip/trip_form.html',{'categories':categories})

    def post(self, request):
        data = request.POST

        try:
            lat = float(event['lat'])
            lng = float(event['lng'])
        except:
            lat = 0
            lng = 0

        
        category = BaseEventCategory.objects.filter(name=data['category'])[0]
        date = data['date']
        date = date.replace('T',' ')
        date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M').date()
        preview = request.FILES.get('preview')
        locations =  json.loads(data['locations'])
        
        event = Trip.objects.create(creater=request.user, description=data['description'],
                                        title=data['title'],preview=preview,date=date, distance=data['distance'],
                                        duration=data['duration'], num_of_places=len(locations),category=category)
        
        for loc in locations:
            location = Location.objects.create(lat=loc['position'][0], lng=loc['position'][1],address=loc['address'], event=event)
       
        events = BaseEvent.objects.all()
        return render(request,"main/main_page.html",{'events':events})


class BaseEventList(View):
    
    def get(self, request):

        keyword = request.GET.get('keyword','')
        sort_option = request.GET.get('sort_option','')
        categories = request.GET.getlist('categories[]','')

        

        
        if(categories != ''):
            events = BaseEvent.objects.filter( ( Q(title__contains=keyword) | Q(description__contains=keyword) ) 
                                            &  Q(category__name__in=categories) )
        else:
            events = BaseEvent.objects.filter( ( Q(title__contains=keyword) | Q(description__contains=keyword) ) 
                                            )

        if(sort_option == 'date'):
            events.order_by('date')
        if(sort_option == 'size'):
            events.order_by('num_of_participants')       
                 
        # paginator = Paginator(events, 9)
        # page = request.GET.get('page',0)


        # events = paginator.get_page(page)
        # print(paginator.num_pages)
        data = render_to_string("main/event_grid.html",{'events':events, 'user':request.user})
        return JsonResponse({'html': data})