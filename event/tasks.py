
from celery.utils.log import get_task_logger
from rel8.celery import app
from django.contrib.auth import get_user_model
from . import models


logger = get_task_logger(__name__)


@app.task()
def activateEvent(eventID):
    "this just activate or deactivate the users"
    logger.info(f' from activateEvent (it Loading' )

    if models.Event.objects.filter(id=eventID).exists():
        logger.info(f' from activateEvent(It Ran)' )
        event = models.Event.objects.get(id =eventID)
        event.is_active=True
        event.save()