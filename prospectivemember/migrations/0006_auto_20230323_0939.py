# Generated by Django 3.2.13 on 2023-03-23 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prospectivemember', '0005_auto_20230323_0924'),
    ]

    operations = [
        migrations.AddField(
            model_name='manprospectivememberformone',
            name='all_raw_materials_used',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='manprospectivememberformone',
            name='all_roduct_manufactured',
            field=models.JSONField(default=list),
        ),
    ]
