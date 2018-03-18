from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

import main.views
import account.views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',main.views.main_page_view),
    path('eventpublish', main.views.EventPublish.as_view(), name='event_publish'),
    path('login', main.views.login, name='login'),
    path('eventinfo/<id>', main.views.event_page, name='event_page'),
    path('account/subscriptions', account.views.subscriptions, name='account'),
    path('account/events', account.views.created_event, name='events'),

    path('eventsuscribe', main.views.EventSubscriptionView.as_view(), name='event_subscribe'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)