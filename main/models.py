import datetime

from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    address = models.CharField(max_length=200, default='')




class EventManager(models.Manager):
    def get_subscriptions(self, subscriber):
        event_subscriptions = EventSubscription.objects.filter(subscriber=subscriber)
        return super().get_queryset().filter(eventsubscription__in=event_subscriptions)



class Event(models.Model):
    creater = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    title = models.CharField(max_length=200, default='')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=False)
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

 
class EventSubscription(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        unique_together = ('subscriber','event')



