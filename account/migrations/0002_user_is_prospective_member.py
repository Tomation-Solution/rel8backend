# Generated by Django 3.2.13 on 2023-03-22 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_prospective_Member',
            field=models.BooleanField(default=False),
        ),
    ]
