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
    path('eventsuscribe', main.views.EventSubscriptionView.as_view(), name='event_subscribe'),
    path('eventedit/<id>', main.views.EventEdit.as_view(), name='event_edit'),
    path('eventdelete/<id>', main.views.event_delete, name='event_delete'),
 	path('trippublish', main.views.TripPublish.as_view(), name='trip_publish'),
    path('logout',main.views.logout, name='logout'),
    path('register',main.views.RegistrationView.as_view(), name='register'),
    path('eventsjson', main.views.BaseEventList.as_view(), name='event_api'),

    path('profile/subscriptions', account.views.subscriptions, name='account'),
    path('profile/edit-profile', account.views.EditProfileView.as_view(), name='edit-profile'),
    path('profile/events', account.views.events, name='events'),
    path('profile/trips', account.views.trips, name='trips'),
    path('profile/<username>', account.views.ProfileView.as_view(), name='profile'),
       
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
