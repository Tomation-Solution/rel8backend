from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models


@receiver(post_save, sender=models.Reminder)
def createJobforReminder(sender,**Kwargs):
    instance = Kwargs['instance']
    if Kwargs['created']:
        instance.schedule_reminder()