# Generated by Django 3.2.13 on 2022-09-13 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.ImageField(default=None, null=True, upload_to='events/image/'),
        ),
    ]
