from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.encoding import force_bytes,force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.core.mail import send_mail
import os,json
from event import models as event_models
from meeting import models as meeting_models
from account.models import user as models_user
from django.db import connection

def activateEmail(user,to_email):
    mail_subject = 'Activate your user account'
    domain_mail = os.environ['domain_mail']
    domain = connection.schema_name+'.'+os.environ['domain']
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

def sendInvitationMail(user,event:event_models.Event,event_proxy_attendies:event_models.EventProxyAttendies):
    mail_subject = f'Invitation for {event.name} Event'
    person_that_invite_you_email= event_proxy_attendies.event_due_user.user.email
    person_that_invite_you_full_name = models_user.Memeber.objects.get(user=event_proxy_attendies.event_due_user.user.id)
    def func(item):return item.get('email')
    to_emails =map(func,event_proxy_attendies.participants)


    domain_mail = os.environ['domain_mail']
    domain = connection.schema_name+'.'+os.environ['domain']
    if connection.schema_name == 'nimn':
        # domain_mail='rel8@members.nimn.com.ng'
        domain = 'https://members.nimn.com.ng'
    data ={
        'person_that_invite_you_email':person_that_invite_you_email,
        'person_that_invite_you_full_name':person_that_invite_you_full_name.full_name,
        'meeting_link_or_address':event.address,
        'name':event.name,
        'short_name':connection.schema_name
        }
    message = render_to_string('proxy_event_mail.html',context=data)

    send_mail(mail_subject,'',domain_mail,recipient_list=to_emails,html_message=message,)



def sendMeetingInvitationMail(user,meeting:meeting_models.Meeting,meeting_proxy_attendies:meeting_models.MeetingProxyAttendies):
    mail_subject = f'Invitation for {meeting.name} Meeting'
    person_that_invite_you_email= meeting_proxy_attendies.member.user.email
    person_that_invite_you_full_name = meeting_proxy_attendies.member.full_name
    def func(item):return item.get('email')
    to_emails =map(func,meeting_proxy_attendies.participants)

    domain_mail = os.environ['domain_mail']
    domain = connection.schema_name+'.'+os.environ['domain']
    if connection.schema_name == 'nimn':
        # domain_mail='rel8@members.nimn.com.ng'
        domain = 'https://members.nimn.com.ng'
    data ={
        'person_that_invite_you_email':person_that_invite_you_email,
        'person_that_invite_you_full_name':person_that_invite_you_full_name.full_name,
        'meeting_link_or_address':meeting.addresse,
        'name':meeting.addresse,
        'short_name':connection.schema_name
        }
    
    message = render_to_string('proxy_meeting_mail.html',context=data)


    send_mail(mail_subject,'',domain_mail,recipient_list=to_emails,html_message=message,)
