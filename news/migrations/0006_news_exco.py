# Generated by Django 3.2.13 on 2022-12-13 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_excorole_chapter'),
        ('news', '0005_alter_news_danload'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='exco',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.excorole'),
        ),
    ]
