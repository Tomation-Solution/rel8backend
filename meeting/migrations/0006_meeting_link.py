# Generated by Django 3.2.13 on 2025-05-05 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0005_meeting_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
