# Generated by Django 3.2.13 on 2023-03-22 22:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_is_prospective_member'),
        ('event', '0003_alter_eventproxyattendies_participants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='exco',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.excorole'),
        ),
    ]
