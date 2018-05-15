from django.contrib import admin
from django.db import models

from .models import Location
from .models import Event
from .models import BaseEvent
from .models import Trip
from .models import Profile
from .models import Comment
from .models import Message
from .models import BaseEventCategory


admin.site.register(Location)
admin.site.register(BaseEvent)
admin.site.register(Trip)
admin.site.register(BaseEventCategory)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(Event)
