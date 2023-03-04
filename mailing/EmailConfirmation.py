from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token
from django.template.loader import render_to_string
import os

def activateEmail(user,to_email):
    mail_subject = 'Activate your user account'
    data = {
        user:user,
        'domain':os.environ['domain'],
        'uid':urlsafe_base64_encode(force_bytes(user.id)),
        'token':account_activation_token.make_token(user=user)
        # 'protocol':'https'
    }
    message = render_to_string('mail_body.html',context=data)
    
    send_mail(mail_subject,'',os.environ['domain_mail'],recipient_list=[to_email],html_message=message,)

