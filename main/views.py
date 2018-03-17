import json

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.contrib import auth
from django.shortcuts import redirect
from django.views import View

from .models import Event
from .models import Location


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


def event_info(request, id):
    pass;



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

        preview = request.FILES.get('preview')
        location = Location.objects.create(lat=lat, lng=lng)
        event = Event.objects.create(location=location, creater=request.user, description=event['description'],title=event['title'],preview=preview)
        return HttpResponse(status=200)

   


    