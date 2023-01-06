from django.shortcuts import render
from Rel8Tenant import models  as tenant_models
import os,json,requests
from rest_framework import viewsets,permissions,status
from utils import permissions  as custom_permissions
from utils.custom_exceptions import CustomError
from django.conf import settings
from utils.usefulFunc import convert_naira_to_kobo
from account.models import user as user_related_models
from . import models as subscription_related_models
from utils.custom_response import Success_response

# Create your views here.
"NOTE the software price is for individual"
SOFTWARE_PRICE = eval(os.environ["software_price"])#we ust get the virtual env data and convert it to the correct number


# def subScribe(request):
#     data = json.loads(request.body)
#     schema_name =data['data']['metadata']['schema_name']
    
#     current_tenant = 



class SubscriptionViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated,]
    # serializer_class = serializers.AdminManageDuesSerializer

    def _checkWhoisToPay(self,request):
        "this func checks what plan a person is paying"
        schema_name =request.tenant.schema_name
        
        current_tenant = tenant_models.Client.objects.get(schema_name=schema_name)
        return current_tenant.payment_plan

    # def _procces_org
    def create(self,request,format=None):
        """
        first of we check if
        """
        amount = 0#amount is equal to 0 but when it the org we mutliply it my the amount of memeber and if it individual we just get the individual amount
        payment_plan =self._checkWhoisToPay(request)
        memberID = None
        forWhat=None
        if payment_plan == 'individual':

            if not request.user.user_type in ['members']:
                raise CustomError({"error":"You must be a member to handle this request"})
            if subscription_related_models.IndividualSubscription.objects.all().filter(is_end=False,is_paid_succesfully=True):
                raise CustomError({"error":"You are Currently On A Subscription"})
            member =  user_related_models.Memeber.objects.get(user=request.user)
            instance,_=subscription_related_models.IndividualSubscription.objects.get_or_create(
                   member=member,
                   is_end=False,is_paid_succesfully=False
            )
            forWhat= 'individualSub'
            amount = SOFTWARE_PRICE
            memberID=member.id
            pk= instance.id

        
        if payment_plan =="organization":
            # we check if this person is an admin
            if not request.user.user_type in ['admin',"super_admin"]:
                raise CustomError({"error":"Please Call the Admin of your Organisation To handle subscription"})
            if subscription_related_models.TenantSubscription.objects.all().filter(is_end=False,is_paid_succesfully=True):
                raise CustomError({"error":"You are Currently On A Subscription"})
            tenant = tenant_models.Client.objects.get(schema_name=request.tenant.schema_name)
            instance,_ = subscription_related_models.TenantSubscription.objects.get_or_create(
                is_end=False,is_paid_succesfully=False,
                tenant=tenant,
            )
            amount = SOFTWARE_PRICE  * user_related_models.Memeber.objects.count()  #number of active member
            forWhat= 'organizationSub'
            pk= instance.id
            print({"pk":pk})
        
        url = 'https://api.paystack.co/transaction/initialize/'
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET}',
            'Content-Type' : 'application/json',
            'Accept': 'application/json',}
        body = {
            "email": request.user.email,
            "amount": convert_naira_to_kobo(amount),
            "metadata":{
                "instanceID":pk,
                'member_id':memberID,
                "user_id":request.user.id,
                "forWhat":forWhat,
                'schema_name':request.tenant.schema_name
            },
            # "callback_url":settings.PAYMENT_FOR_MEMBERSHIP_CALLBACK,
            }
        try:
            resp = requests.post(url,headers=headers,data=json.dumps(body))
        except requests.ConnectionError:
            raise CustomError({"error":"Network Error"},status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
  
        if  resp.status_code ==200:
            data = resp.json()
            instance.paystack_key= data['data']['reference']
            instance.save()

            return Success_response(msg='Success',data=data)

        raise CustomError(message={"error":'Some Error Occured Please Try Again'},status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
