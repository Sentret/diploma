from django.contrib import admin

from .models import Location
from .models import Event
from .models import BaseEvent
from .models import Trip
from .models import Profile

admin.site.register(Location)
admin.site.register(BaseEvent)
admin.site.register(Profile)
