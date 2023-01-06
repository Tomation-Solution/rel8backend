from email.policy import default
from django.db import models,connection
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from utils.usefulFunc import get_localized_time
import json
from pytz import timezone

# Create your models here.


class Reminder(models.Model):
    title = models.CharField(max_length=400)
    body = models.TextField()
    start_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    is_active= models.BooleanField(default=False)

    def schedule_reminder(self):
        'set a timer to this instance'
        tenant = connection.tenant
        localtz = timezone('Africa/Lagos')
        localized_time = get_localized_time(
            self.start_date, self.start_time, localtz
        )

        clocked, _ = ClockedSchedule.objects.get_or_create(
            clocked_time=localized_time
        )
        PeriodicTask.objects.create(
            clocked=clocked,
            name=f"{str(self.id)} active",  # task name
            task="reminders.tasks.set_reminder_to_active",  # task.
            args=json.dumps(
                [
                    self.id,
                ]
            ),  # arguments
            description="this changes the reminder to acitive",
            one_off=True,
            headers=json.dumps(
                {
                    "_schema_name": tenant.schema_name,
                    "_use_tenant_timezone": True,
                }
            ),
        )
