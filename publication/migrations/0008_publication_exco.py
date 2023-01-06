# Generated by Django 3.2.13 on 2022-12-13 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_excorole_chapter'),
        ('publication', '0007_alter_publication_danload'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='exco',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.excorole'),
        ),
    ]
