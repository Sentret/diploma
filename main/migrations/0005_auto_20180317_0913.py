# Generated by Django 2.0.3 on 2018-03-17 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20180317_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='preview',
            field=models.ImageField(default='', upload_to='previews'),
        ),
    ]