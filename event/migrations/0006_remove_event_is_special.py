# Generated by Django 3.2.13 on 2023-06-26 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_event_is_special'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='is_special',
        ),
    ]
