# Generated by Django 3.2.13 on 2023-02-07 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_membershipgrade'),
        ('news', '0003_news_dues_for_membership_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='dues_for_membership_grade',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.membershipgrade'),
        ),
        migrations.AlterField(
            model_name='news',
            name='exco',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.excorole'),
        ),
    ]