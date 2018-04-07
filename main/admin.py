from django.contrib import admin

from .models import Location
from .models import Event
from .models import BaseEvent
from .models import Trip

admin.site.register(Location)
admin.site.register(BaseEvent)
