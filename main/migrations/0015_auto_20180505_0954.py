# Generated by Django 2.0.4 on 2018-05-05 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_trip_num_of_placess'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trip',
            old_name='num_of_placess',
            new_name='num_of_places',
        ),
    ]
