# Generated by Django 3.2.13 on 2022-08-19 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Minute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(default=None, null=True, upload_to='minute/%d/')),
                ('name', models.CharField(default=' ', max_length=300)),
                ('chapter', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.chapters')),
            ],
        ),
    ]
