from __future__ import print_function
import sib_api_v3_sdk
from django.conf import settings
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from django.template.loader import render_to_string
from django.core.mail import send_mail



from mailing.services.mailing import Mailing, MailException


class SendInBlue(Mailing):
    apiKey = settings.SENDINBLUE_API_KEY
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = apiKey

    @classmethod
    def send_email(cls, sender, to, subject, html_content, reply_to=None):
        """
        This function takes the details of the email to be sent,
        and sends it using the sendinblue API.
        """
        if reply_to is not None:
            reply_to = reply_to

        try:
            send_mail(subject=subject,message='',html_message=html_content,from_email=sender,recipient_list=[to])
        except :
            raise MailException(
                "Exception when calling SMTPApi->send_transac_email: %s\n" % e
            )
