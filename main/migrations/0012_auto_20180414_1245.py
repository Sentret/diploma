# Generated by Django 2.0.4 on 2018-04-14 12:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='addresser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='addresser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='recipient', to=settings.AUTH_USER_MODEL),
        ),
    ]