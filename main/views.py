import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
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
    return render(request,"main/main_page.html")


class EventPublish(View):
    def get(self, request):
        return render(request,"main/event_form.html")

    def post(self, request):
        event = json.loads(request.body)
        location = Location.objects.create(lat=event['lat'], lng=event['lng'])
        event = Event.objects.create(location=location, creater=request.user, description=event['description'],title=event['title'])
        return HttpResponse(status=200)





    