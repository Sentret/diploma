from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

import main.views
import account.views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',main.views.main_page_view, name='main-page'),
    path('eventpublish', main.views.EventPublish.as_view(), name='event_publish'),
    path('login', main.views.login, name='login'),
    path('eventinfo/<id>', main.views.event_page, name='event_page'),
    path('account/subscriptions', account.views.subscriptions, name='account'),
    path('account/events', account.views.created_by_user_events, name='events'),
    path('eventsuscribe', main.views.EventSubscriptionView.as_view(), name='event_subscribe'),
    path('eventedit/<id>', main.views.EventEdit.as_view(), name='event_edit'),
    path('eventdelete/<id>', main.views.event_delete, name='event_delete'),
 	path('trippublish', main.views.TripPublish.as_view(), name='trip_publish'),
       
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
