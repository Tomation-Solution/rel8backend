# import os
from django.db import connection
from django.template.loader import render_to_string
from mymailing.views import send_mail

def send_technical_contact_us_mail(data):
    schema_name = data.get('schema_name')
    sender_email = data.get('sender_email')
    sender_name = data.get('sender_name')

    connection.set_schema(schema_name=schema_name)
    mail_subject =f'{schema_name.upper()} Technical Contact Us'
    

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


def send_admin_contact_us_mail(data):
    schema_name = data.get('schema_name')
    sender_email = data.get('sender_email')
    sender_name = data.get('sender_name')

    connection.set_schema(schema_name=schema_name)
    mail_subject =f'{schema_name.upper()} Admin Contact Us'
    

    data = {
         'sender_name':sender_name,
         'sender_email': sender_email,
         'message': data.get('message')
    }
    html_content = render_to_string('admin_contactus.html',context=data)

    send_mail(
        subject=mail_subject,
        html_content=html_content,
        to=[
            {"email": 'dbadebayo@gmail.com',"name": 'Adebayo'},
            {"email": 'info@bukaa.org',"name": 'Bukaa Admin'},
            {"email": 'msismail.reg@buk.edu.ng',"name": 'Ismail'}
        ],
        sender={"name":sender_name,"email":sender_email}
    )