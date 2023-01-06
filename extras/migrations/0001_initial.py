# Generated by Django 3.2.13 on 2023-01-06 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryV2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('date_taken', models.DateField()),
                ('chapters', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.chapters')),
            ],
        ),
        migrations.CreateModel(
            name='Ticketing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=300)),
                ('body', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ImagesForGalleryV2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='gallery_v2/')),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='extras.galleryv2')),
            ],
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.TextField()),
                ('photo_file', models.ImageField(upload_to='gallery/')),
                ('name', models.CharField(max_length=300)),
                ('chapters', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.chapters')),
            ],
        ),
    ]
