# import os
from django.db import connection
from django.template.loader import render_to_string
from mymailing.views import send_mail

def send_contact_us_mail(data):
    'send forgot password notifcation'
    schema_name = data.get('schema_name')
    sender_email = data.get('sender_email')
    sender_name = data.get('sender_name')

    connection.set_schema(schema_name=schema_name)
    mail_subject =f'{schema_name.upper()} Contact Us'
    # domain_mail = os.environ['domain_mail']
    # sender_email = domain_mail
    

    data = {
         'sender_name':sender_name,
         'sender_email': sender_email,
         'message': data.get('message')
    }
    html_content = render_to_string('contactus.html',context=data)

    send_mail(
        subject=mail_subject,
        html_content=html_content,
        to=[
            {"email": 'dbadebayo@gmail.com',"name": 'Adebayo'},
            {"email": 'harof.dev@gmail.com',"name": 'Arafat'},
            {"email": 'samuelayo61@gmail.com',"name": 'Samuel'}
        ],
        sender={"name":sender_name,"email":sender_email}
    )