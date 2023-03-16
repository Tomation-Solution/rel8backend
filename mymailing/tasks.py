from celery import shared_task
from django.contrib.auth import get_user_model

from .EmailConfirmation import activateEmail,sendInvitationMail

from event.models import Event,EventProxyAttendies

@shared_task()
def send_activation_mail(user_id,to_email):
    user = get_user_model().objects.get(id=user_id)
    activateEmail(user,to_email)

@shared_task()
def send_event_invitation_mail(user_id,event_id,event_proxy_attendies_id):
    user = get_user_model().objects.get(id=user_id)
    event =Event.objects.get(id=event_id)
    event_proxy_attendies= EventProxyAttendies.objects.get(id=event_proxy_attendies_id)
    sendInvitationMail(
        user=user,
        event=event,
        event_proxy_attendies=event_proxy_attendies
    )