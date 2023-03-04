from celery import shared_task
from django.contrib.auth import get_user_model
from .EmailConfirmation import activateEmail



@shared_task()
def send_activation_mail(user_id,to_email):
    user = get_user_model().objects.get(id=user_id)
    activateEmail(user,to_email)


