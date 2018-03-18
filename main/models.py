import datetime

from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
	lat = models.FloatField()
	lng = models.FloatField()
	address = models.CharField(max_length=200, default='')


class Event(models.Model):
	creater = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
	title = models.CharField(max_length=200, default='')
	location = models.ForeignKey(Location, on_delete=models.CASCADE, null=False)
	description = models.TextField()
	preview = models.ImageField(default='',upload_to='previews')
	date = models.DateField(default=datetime.date.today)

	def __str__(self):
		return self.title

 
class EventSubscription(models.Model):
	subscriber = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
	event = models.ForeignKey(Event, on_delete=models.DO_NOTHING, null=True)

	class Meta:
		unique_together = ('subscriber','event')



