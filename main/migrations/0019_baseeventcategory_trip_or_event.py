# Generated by Django 2.0.4 on 2018-05-12 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20180506_0526'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseeventcategory',
            name='trip_or_event',
            field=models.CharField(default='Event', max_length=200),
        ),
    ]
