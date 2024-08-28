# Generated by Django 4.2.15 on 2024-08-28 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("event", "0009_publicevent_paystack_key_publicevent_registered_at_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="publicevent",
            name="paystack_key",
        ),
        migrations.CreateModel(
            name="PublicEventPayment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("paystack_key", models.CharField(default="", max_length=250)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="event.publicevent",
                    ),
                ),
            ],
        ),
    ]
