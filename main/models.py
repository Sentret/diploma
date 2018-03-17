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

	def __str__(self):
		return self.title


