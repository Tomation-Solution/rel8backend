from django.shortcuts import render
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_decode

from utils.custom_exceptions import CustomError
from .tokens import account_activation_token
from utils.custom_response import Success_response
from rest_framework import status
# from .EmailConfirmation import forgot_passwordEmail


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
        raise CustomError({'error':'Token Is Invalid'},)





# @api_view(['POST'])
# def request_forgot_password(request):
#     user_email = request.data.get('email',None)
#     if user_email:
#         user = None
#         if(get_user_model().objects.filter(email=user_email).exists()):
#             user= get_user_model().objects.get(email=user_email)
#             forgot_passwordEmail(user=user,to_email=user_email) #this would send the email
#             return Success_response("please check your email for steps to change password",[]) 

#         else:
#             raise CustomError({'error':'This email has not been registered in Sequential'}) 


#     else:
#         raise CustomError({'error':'Please a valid email'}) 


# @api_view(['POST'])
# def reset_password(request,uidb64,token):
#     User = get_user_model()

#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(id=uid)

#     except:
#         user=None
#     if(user is not None and account_activation_token.check_token(user,token)):
#         password = request.data.get('password',None)
#         if(password):
#             user.set_password(password)
#             user.save()
#             return Success_response("Password Rest Successfully",[]) 
#         else:raise CustomError({'error':'Invalid Payload. Password is meant to be sent'}) 
#     else:
#         raise CustomError({'error':'Token Is Invalid'}) 

