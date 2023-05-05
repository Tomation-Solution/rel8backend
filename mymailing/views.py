from django.shortcuts import render
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token
from utils.custom_response import Success_response
from rest_framework import status
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
# from .EmailConfirmation import forgot_passwordEmail
from utils.custom_exceptions import CustomError
import os


@authentication_classes([])
@permission_classes([])
@api_view(['GET'])
def activate_user(request,uidb64,token):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)

    except:
        user=None
    if(user is not None and account_activation_token.check_token(user,token)):
        user.is_active=True
        user.save()
        return Success_response("Thank you for your email confirmation. Now  you can login your account",[]) 
    else:
        raise CustomError({'error':'Token Is Invalid',})



def send_mail(subject,html_content,sender,to):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key']=os.environ['SENDINBLUE_API_KEY']
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,html_content=html_content,
        sender=sender, subject=subject)
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
