import json

from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.db.models import Q

from main.models import Message


def room(request, room_name):

    addresser_id = int( int(room_name) / request.user.id )   
    addresser = User.objects.get(pk=addresser_id)

    messages = Message.objects.filter( Q(addresser=addresser, recipient=request.user) | 
                                       Q(addresser=request.user, recipient=addresser))


    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'messages':messages,
        'addresser':addresser
    })