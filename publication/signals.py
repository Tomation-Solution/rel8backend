from django.dispatch import receiver
from django.db.models.signals import post_save
from . import models
from LatestUpdate import models as lastest_update_models


@receiver(post_save,sender=models.Publication)
def update_latest_updatemodel(sender,**kwargs):
    pub  = kwargs['instance']
    lastest_update_models.LastestUpdates.objects.manage_publication(pub)