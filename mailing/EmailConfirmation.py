from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token
from django.template.loader import render_to_string
import os
from django.db import connection

def activateEmail(user,to_email):
    mail_subject = 'Activate your user account'

    domain_mail = os.environ['domain_mail']
    domain = os.environ['domain']
    if connection.schema_name == 'nimn':
        # domain_mail='rel8@members.nimn.com.ng'
        domain = 'https://members.nimn.com.ng'
    data = {
        user:user,
        'domain':domain,
        'uid':urlsafe_base64_encode(force_bytes(user.id)),
        'token':account_activation_token.make_token(user=user)
        # 'protocol':'https'
    }
    message = render_to_string('mail_body.html',context=data)

    send_mail(mail_subject,'',domain_mail,recipient_list=[to_email],html_message=message,)

