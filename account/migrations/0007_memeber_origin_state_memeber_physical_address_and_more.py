# Generated by Django 4.2.15 on 2024-08-13 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0006_memeber_department_memeber_name_memeber_yog_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="memeber",
            name="origin_state",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name="memeber",
            name="physical_address",
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name="memeber",
            name="residential_country",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="memeber",
            name="residential_state",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="memeber",
            name="title",
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
