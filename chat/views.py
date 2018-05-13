import json

from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from main.models import Message



def room(request, room_name):

    try:
        addresser_id = int(room_name) / request.user.id 
    except:
        HttpResponse(status=404)
    addresser = get_object_or_404(User, pk=addresser_id)

    messages = Message.objects.filter( Q(addresser=addresser, recipient=request.user) | 
                                       Q(addresser=request.user, recipient=addresser)).order_by('date')


    
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'messages':messages,
        'addresser':addresser
    })