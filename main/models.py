import datetime

from django.db import models
from django.contrib.auth.models import User


class EventManager(models.Manager):
    def get_subscriptions(self, subscriber):
        event_subscriptions = EventSubscription.objects.filter(subscriber=subscriber)
        return super().get_queryset().filter(eventsubscription__in=event_subscriptions)


class BaseEventCategory(models.Model):
    name = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.name


class BaseEvent(models.Model):
    creater = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    title = models.CharField(max_length=200, default='')
    description = models.TextField()
    num_of_participants = models.IntegerField(default=0)
    preview = models.ImageField(default='',upload_to='previews')
    date = models.DateTimeField(default=datetime.date.today)
    category = models.ForeignKey(BaseEventCategory, on_delete=models.DO_NOTHING, null=True, blank=True)
    event_manager = EventManager()
    objects = models.Manager()


    def subscribe(self, user):
        subscription = EventSubscription.objects.create(subscriber=user, event=self)
        self.num_of_participants +=1
        self.save()


    def unsubscribe(self, user):
        subscription = EventSubscription.objects.all().filter(subscriber=user, event=self)
        self.num_of_participants -=1
        self.save()
        subscription.delete()


    def is_user_subscribed(self, user):
        num_of_subscribers = EventSubscription.objects.all().filter(subscriber=user, event=self).count()
        return num_of_subscribers ==1


    def get_subscribers(self):
        return EventSubscription.objects.filter(event=self)

    def __str__(self):
        return self.title
    

class Event(BaseEvent):
    pass
    

class Trip(BaseEvent):
    distance = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    num_of_places = models.IntegerField(default=0)


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
    date = models.DateTimeField(auto_now=True)
    parrent = models.ForeignKey("Comment", on_delete=models.DO_NOTHING, null=True) 


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    avatar = models.ImageField(default='/avatars/default-avatar.png',upload_to='avatars')
    about = models.TextField(default='')
    age = models.IntegerField(default=0)


class Message(models.Model):
    addresser = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, related_name='addresser')
    recipient = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, related_name='recipient')
    message = models.TextField()


