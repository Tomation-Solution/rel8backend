# Generated by Django 3.2.13 on 2023-06-23 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extras', '0003_alter_fundaproject_what_project_needs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supportprojectincash',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]