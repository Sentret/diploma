import json

from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404

from main.models import Message
from account.pairing import inverse_cantor_pairing


def room(request, room_name):

    inverse_cantor = inverse_cantor_pairing(int(room_name))
    inverse_cantor.remove(request.user.id)

    addresser_id = inverse_cantor[0] 
    addresser = get_object_or_404(User, pk=addresser_id)

    messages = Message.objects.filter( Q(addresser=addresser, recipient=request.user) | 
                                       Q(addresser=request.user, recipient=addresser)).order_by('date')


    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'messages':messages,
        'addresser':addresser
    })