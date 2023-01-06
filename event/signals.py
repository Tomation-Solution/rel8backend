from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models



@receiver(post_save, sender=models.Event)
def create_event_job(sender, **kwargs):
    instance = kwargs['instance']
    if kwargs['created']:
        instance.create_event_job()
