# Generated by Django 5.1.4 on 2025-01-16 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='is_for_members_only',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
