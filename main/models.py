import datetime

from django.db import models
from django.contrib.auth.models import User


class EventManager(models.Manager):
    def get_subscriptions(self, subscriber):
        event_subscriptions = EventSubscription.objects.filter(subscriber=subscriber)
        return super().get_queryset().filter(eventsubscription__in=event_subscriptions)



class BaseEvent(models.Model):
    creater = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    title = models.CharField(max_length=200, default='')
    description = models.TextField()
    preview = models.ImageField(default='',upload_to='previews')
    date = models.DateTimeField(default=datetime.date.today)
    event_manager = EventManager()
    objects = models.Manager()


    def subscribe(self, user):
        subscription = EventSubscription.objects.create(subscriber=user, event=self)


    def unsubscribe(self, user):
        subscription = EventSubscription.objects.all().filter(subscriber=user, event=self)
        subscription.delete()


    def is_user_subscribed(self, user):
        subscription = EventSubscription.objects.all().filter(subscriber=user, event=self)
        # статус 
        subscribed = False
        if(subscription.count()==1):
            subscribed = True
        return subscribed

    def __str__(self):
        return self.title
    

class Event(BaseEvent):
    pass
    


class Trip(BaseEvent):
    pass


class Location(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    address = models.CharField(max_length=200, default='')
    event = models.ForeignKey(BaseEvent, on_delete=models.CASCADE, default=None)


class EventSubscription(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    event = models.ForeignKey(BaseEvent, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        unique_together = ('subscriber','event')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    event = models.ForeignKey(BaseEvent, on_delete=models.DO_NOTHING, null=True)
    content = models.TextField()
    date = models.DateTimeField(default=datetime.date.today)
    parrent = models.ForeignKey("Comment", on_delete=models.DO_NOTHING, null=True) 


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    avatar = models.ImageField(default='/avatars/default-avatar.png',upload_to='avatars')