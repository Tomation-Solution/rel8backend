
from celery.utils.log import get_task_logger
from rel8.celery import app
from django.contrib.auth import get_user_model
from . import models

logger = get_task_logger(__name__)




@app.task()
def endSub(id,subType):
    logger.info(f'{subType} with {id} from matthew' )

    if subType == 'individual':
        if models.IndividualSubscription.objects.filter(id =id).exists():
            "let check if we even have a subcription with this id if yes let row"
            individualSUb = models.IndividualSubscription.objects.get(id=id)
            individualSUb.is_end=True
            individualSUb.save()

    if subType == 'organization':
        if models.TenantSubscription.objects.filter(id =id).exists():
            "let check if we even have a subcription with this id if yes let row"
            TenantSUb = models.TenantSubscription.objects.get(id=id)
            TenantSUb.is_end=True
            TenantSUb.save()
    # if subType == 'organization':