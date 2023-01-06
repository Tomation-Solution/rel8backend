from rel8.celery import app

from mailing.services.mailing import MailException
from mailing.services.send_in_blue import SendInBlue
from django.core.mail import EmailMultiAlternatives
from anymail.message import attach_inline_image_file

# @app.task()
def send_confirmation_email(sender: dict, content: str, first_name: str, last_name: str, recipient_email: list):
    """
    A function that sends a confirmation email
    Args:
        sender: the sender of the email
        first_name:
        content:
        last_name:
        recipient_email:
    Returns:

    """
    subject = f"Hi! {first_name} {last_name} Email Confirmation from Anni"

    try:
        SendInBlue.send_email(sender=sender, to=recipient_email, subject=subject, html_content=content)
    except:
        from account.models import User
        from mailing.models import EmailInvitation


        print(f"deleting user with email: {recipient_email}")
        EmailInvitation.objects.filter(email=recipient_email).delete()
        User.objects.filter(email=recipient_email).delete()
        print(f"deleted user with email: {recipient_email}")
