# Generated by Django 3.2.13 on 2023-03-23 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_is_prospective_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('admin', 'Admin'), ('super_admin', 'Super Admin'), ('members', 'Members'), ('prospective_members', 'Prospective Members')], max_length=25),
        ),
    ]
