# Generated by Django 3.2.13 on 2023-06-26 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_alter_event_exco'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_special',
            field=models.BooleanField(default=False),
        ),
    ]
