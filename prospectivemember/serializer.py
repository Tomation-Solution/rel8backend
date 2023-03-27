from rest_framework import serializers
from .models import man_prospective_model
from django.contrib.auth import get_user_model as USER
from utils.custom_exceptions import  CustomError 
from mymailing import tasks as mymailing_task
from rest_framework.authtoken.models import Token
from Rel8Tenant import models as rel8tenant_related_models
import requests,json
from utils.usefulFunc import convert_naira_to_kobo
from prospectivemember.models.man_prospective_model import ManProspectiveMemberProfile,RegistrationAmountInfo
from utils.custom_response import Success_response
from rest_framework import status

class CreateManPropectiveMemberSerializer(serializers.ModelSerializer):

    def _process_paymentlink(self,request,user):

        schema_name = request.tenant.schema_name
        client_tenant = rel8tenant_related_models.Client.objects.get(schema_name=schema_name)
        if client_tenant.paystack_secret == 'null' or client_tenant.paystack_publickey == 'null':
            raise CustomError({'error':'Paystack not active please reach out to the developer'})
        PAYSTACK_SECRET = client_tenant.paystack_secret
        instance =None
        url = 'https://api.paystack.co/transaction/initialize/'
        headers = {
        'Authorization': f'Bearer {PAYSTACK_SECRET}',
        'Content-Type' : 'application/json',
        'Accept': 'application/json',}
        reg = RegistrationAmountInfo.objects.all().first()
        if reg is None:
            raise CustomError({'error':'please reach out to your admin to set the amount to be paid'})
        instance = ManProspectiveMemberProfile.objects.get(user=user)
        member = instance
        amount_to_be_paid = reg.amount
        pk= instance.id
        if instance.has_paid:
            raise CustomError({'error':'Please hold for admin to process your info you have paid already'})

        body = {
            "email": user.email,
            "amount": convert_naira_to_kobo(amount_to_be_paid),
            "metadata":{
                "instanceID":pk,
                'member_id':member.id,
                "user_id":user.id,
                "forWhat":'prospective_member_registration',
                'schema_name':request.tenant.schema_name,
                'user_type':user.user_type,
                'amount_to_be_paid':str(amount_to_be_paid)
            },
            # "callback_url":settings.PAYMENT_FOR_MEMBERSHIP_CALLBACK,
            }

        try:
            resp = requests.post(url,headers=headers,data=json.dumps(body))
        except requests.ConnectionError:
            raise CustomError({"error":"Network Error"},status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
        if resp.status_code ==200:
            data = resp.json()
            instance.paystack_key= data['data']['reference']
            instance.save()
            return data

        raise CustomError(message='Some Error Occured Please Try Again',status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    

    def create(self, validated_data):
        email = validated_data.get('email',None)
        cac = validated_data.get('cac_registration_number')
        if USER().objects.filter(email=email).exists():
            raise CustomError({'error':'user email already exists'})
        user = USER().objects.create_user(
            email=email,
            password=cac,
            user_type='prospective_members'
        )
        user.is_active = True
        user.is_prospective_Member=True
        user.save()

        man_propective = man_prospective_model.ManProspectiveMemberProfile.objects.create(
            user=user,
            **validated_data
        )
        mymailing_task.send_activation_mail.delay(user.id,user.email)
       
       
        token,created =Token.objects.get_or_create(user=user)
        payment_info = self._process_paymentlink(self.context.get('request'),user)
        return {
                "user_type":user.user_type,
                'token':token.key,
                'has_paid':user.manprospectivememberprofile.has_paid,
                'prospective_member_id':user.manprospectivememberprofile.id,
                'payment_info':payment_info
            }
    class Meta:
        model  =man_prospective_model.ManProspectiveMemberProfile
        fields = '__all__'
        read_only_fields = ['user','paystack','has_paid']


class PropectiveMemberManageFormOneSerializer(serializers.ModelSerializer):

    def create(self, validated_data):return None

    class Meta:
        model = man_prospective_model.ManProspectiveMemberFormOne
        fields = '__all__'
        read_only_fields =['prospective_member']

    
class PropectiveMemberManageFormTwoSerializer(serializers.ModelSerializer):

    def create(self, validated_data):return None
    class Meta:
        model = man_prospective_model.ManProspectiveMemberFormTwo
        fields = '__all__'
        read_only_fields =['prospective_member']

    

