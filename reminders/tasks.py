from rel8.celery import app
from . import models
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@app.task()
def set_reminder_to_active(reminder_id):
    logger.info(f'hello world')
    reminder = models.Reminder.objects.get(id=reminder_id)
    logger.info(f'{reminder_id} that the id  title:{reminder.title}')
    reminder.is_active=True
    reminder.save()
    