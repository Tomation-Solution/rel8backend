from django.urls import reverse
from utils.custom_exceptions import CustomError
from utils.custom_response import Success_response
from rest_framework import status,authentication,permissions
from rest_framework.decorators import api_view,permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import get_object_or_404

from .. import models
from event import models as event_models
import requests,json
from rest_framework.views import APIView
from utils import permissions as custom_permissions
from utils.usefulFunc import convert_naira_to_kobo
from account.models import user as user_model
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.db import connection
from subscription import models as subscription_related_models
from Rel8Tenant import models as rel8tenant_related_models
from account.models.user import Memeber
from django.contrib.auth import get_user_model
from extras  import models as extras_models
from prospectivemember.models.man_prospective_model import ManProspectiveMemberProfile,RegistrationAmountInfo
from mymailing import tasks as mymailing_task
from prospectivemember.models import general as generalProspectiveModels
from django.shortcuts import get_object_or_404
from event.models import EventProxyAttendies
from mymailing import tasks as mailing_tasks
import threading
from utils.extraFunc import generate_n
from .. import serializers
from utils import custom_response



def very_payment(request,reference=None):
    # this would be in the call back to check if the payment is a success
    if reference is None:
        raise CustomError({"error":"You need to send a refrence back"})
    schema_name = request.tenant.schema_name
    client_tenant = rel8tenant_related_models.Client.objects.get(schema_name=schema_name)
    
    # this is checking if the user has pluged his paystack account 
    if client_tenant.paystack_secret == 'null' or client_tenant.paystack_publickey == 'null':
        raise CustomError({'error':'Paystack not active please reach out to the developer'})

    PAYSTACK_SECRET = client_tenant.paystack_secret

    url = f'https://api.paystack.co/transaction/verify/{reference}'
    headers = {
    'Authorization': f'Bearer {PAYSTACK_SECRET}',
    'Content-Type' : 'application/json',
    'Accept': 'application/json',
    }
    try:
        resp = requests.get(url,headers=headers)
    except requests.ConnectionError:
        raise CustomError({"error":"Nework Error"}) 

    if resp.json()['data']['status'] == 'success':
        return Success_response(msg="Verified the payment Successfully",)

    raise CustomError({"error":"Something went wrong, try Again"})

 
class DuesPaymentView(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes=[
        permissions.IsAuthenticated,
        custom_permissions.IsMemberOrProspectiveMember]

    def generateMetaData(self,request,forWhat='due',pk=None):
        """
        'this function generate payment meta data and amount to be paid'
        forWhat can be  = due,event,deactivating_due
        """
        if forWhat == 'prospective_member_registration':
            # it will be only on instance that will ever exist
            if connection.schema_name == 'man':
                reg = RegistrationAmountInfo.objects.all().first()
                if reg is None:
                    raise CustomError({'error':'please reach out to your admin to set the amount to be paid'})
                instance =get_object_or_404(ManProspectiveMemberProfile,user=request.user)
                amount_to_be_paid = reg.amount
                pk= instance.id
                if instance.has_paid:
                    raise CustomError({'error':'Please hold for admin to process your info you have paid already'})
            else:
                rule = generalProspectiveModels.AdminSetPropectiveMembershipRule.objects.all().first()
                if rule is None:
                    raise CustomError({'error':'please reach out to your admin to set the amount to be paid'})
                instance = get_object_or_404(generalProspectiveModels.ProspectiveMemberProfile,user=request.user)
                amount_to_be_paid = rule.amount
                pk= instance.id
                if instance.has_paid:
                    raise CustomError({'error':'Please hold for admin to proces your info because you have paid already'})

        if forWhat=="due":
            try:
                due_instance = models.Due.objects.get(id=pk)
            except models.Due.DoesNotExist:
                raise CustomError({"error":"Due does not exist"})

            if models.Due_User.objects.filter(due=due_instance, user=request.user).exists(): raise CustomError({"error":"you have paid for this due already"})

            amount_to_be_paid = due_instance.amount

        if forWhat =='deactivating_due':
            try:
                due_instance = models.DeactivatingDue.objects.get(id=pk)
            except models.DeactivatingDue.DoesNotExist:
                raise CustomError({"error":"Deactivating Due does not exist"})

            if models.DeactivatingDue_User.objects.filter(deactivatingdue=due_instance, user=request.user).exists(): raise CustomError({"error":"you have paid for this deactivating due already"})

            amount_to_be_paid = due_instance.amount

        if request.user.user_type== 'members':
            member = user_model.Memeber.objects.get(user=request.user)
        if request.user.user_type== 'prospective_members':
            if connection.schema_name == 'man':
                member =ManProspectiveMemberProfile.objects.get(user=request.user)
            else:
                member = generalProspectiveModels.ProspectiveMemberProfile.objects.get(user=request.user)


        return {
            'amount': str(amount_to_be_paid),
            'metadata':{
                "id":pk,
                'member_id': member.id,
                "user_id":request.user.id,
                "forWhat":forWhat,
                'schema_name':request.tenant.schema_name,
                'user_type':request.user.user_type
            }
        }

    def post(self, request, forWhat="due",pk=None):

        schema_name = request.tenant.schema_name
        client_tenant = rel8tenant_related_models.Client.objects.get(schema_name=schema_name)
        if client_tenant.paystack_secret == 'null' or client_tenant.paystack_publickey == 'null':
            raise CustomError({'error':'Paystack Key not active please reach out to the developer'})
       
        PAYSTACK_SECRET = client_tenant.paystack_secret

        generateInfo = self.generateMetaData(request,forWhat,pk)
        # Paystack intialization Url
        url = 'https://api.paystack.co/transaction/initialize/'
        headers = {
            'Authorization': f'Bearer {PAYSTACK_SECRET}',
            'Content-Type' : 'application/json',
            'Accept': 'application/json',}
        body = {
            "email": request.user.email,
            "amount": convert_naira_to_kobo(generateInfo.get('amount')),
            "metadata":generateInfo.get('metadata'),
            "callback_url": request.data.get('callback_url')
            }
        try:
            resp = requests.post(url,headers=headers,data=json.dumps(body))
        except requests.ConnectionError:
            raise CustomError({"error":"Network Error"},status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
        if resp.status_code in [200, 201]:
            data = resp.json()
            return Success_response(msg='Success. Payment in progress...', data=data)
        
class SaveDuesPayment(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serialzed = serializers.DueUserSerializer(data=request.data)
        serialzed.is_valid(raise_exception=True)
        data = serialzed.save(user=request.user, is_paid=True)

        return custom_response.Success_response(msg='Saved due payment details', data=[], status_code=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        due_id = request.query_params.get('id')
        if due_id:
            # Retrieve the specific due payment by ID
            due_payment = get_object_or_404(models.DueUser, id=due_id)
            clean_data = serializers.DueUserSerializer(due_payment)
            return custom_response.Success_response(msg='Success', data=clean_data.data, status_code=status.HTTP_200_OK)
        else:
            # Return all due payments
            due_payments = models.DueUser.objects.all()
            clean_data = serializers.DueUserSerializer(due_payments, many=True)
            return custom_response.Success_response(msg='Success', data=clean_data.data, status_code=status.HTTP_200_OK)

class SaveDeactivatingDuesPayment(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serialzed = serializers.DeactivatingDueUserSerializer(data=request.data)
        serialzed.is_valid(raise_exception=True)
        data = serialzed.save(user=request.user, is_paid=True)

        return custom_response.Success_response(msg='Saved deactivating due payment details', data=[], status_code=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        due_id = request.query_params.get('id')
        if due_id:
            # Retrieve the specific deactivating due payment by ID
            deactivating_due_payment = get_object_or_404(models.DeactivatingDueUser, id=due_id)
            clean_data = serializers.DeactivatingDueUserSerializer(deactivating_due_payment)
            return custom_response.Success_response(msg='Success', data=clean_data.data, status_code=status.HTTP_200_OK)
        else:
            # Return all deactivating due payments
            deactivating_due_payments = models.DeactivatingDueUser.objects.all()
            clean_data = serializers.DeactivatingDueUserSerializer(deactivating_due_payments, many=True)
            return custom_response.Success_response(msg='Success', data=clean_data.data, status_code=status.HTTP_200_OK)

        # # since the payment was a success then we reduce the amount owing in memeber profile
        # member_profile = Memeber.objects.get(user=user)
        # member_profile.amount_owing = member_profile.amount_owing + due.amount
        # member_profile.save()

def webhookPayloadhandler(meta_data,user,):
        
        if meta_data['forWhat'] == 'due':
            # instanceID in this context means Due_User id
            due = models.Due_User.objects.get(user=user,id=meta_data['instanceID'])
            due.is_paid=True
            due.save()
            # since the payment was a success then we reduce the amount owing in memeber profile
            member_profile = Memeber.objects.get(user=user)
            member_profile.amount_owing= member_profile.amount_owing + due.amount
            member_profile.save()

        if meta_data['forWhat'] == 'deactivating_due':
            # instanceID in this context means Due_User id
            due = models.DeactivatingDue_User.objects.get(user=user,id=meta_data['instanceID'])
            due.is_paid=True
            due.save()    
        if meta_data['forWhat'] =='event_payment':
            event_user = event_models.EventDue_User.objects.get(user=user,id=meta_data['instanceID'])
            event_user.is_paid=True
            event_user.save()
#Note setTimer set the subscription so it would end at a given time
        if meta_data['forWhat'] =='individualSub':
            CurrentTenant  = rel8tenant_related_models.Client.objects.get(schema_name=meta_data['schema_name'])
            # the payment means a memebers is trying to subscribe
            member = user_model.Memeber.objects.get(id=meta_data.get('member_id'))
            individualSub = subscription_related_models.IndividualSubscription.objects.get(
            # member=member,
            id =meta_data.get('instanceID'))
            # this means the payment was succesfful
            individualSub.is_paid_succesfully=True
            # this would be false for now our periodic task will set it to true meaning th sub has ended
            individualSub.is_end=False
            individualSub.save()
            subscription_related_models.setTimer(meta_data.get('instanceID'),"individual",meta_data['schema_name'],CurrentTenant)

 
        if meta_data['forWhat'] =='organizationSub':
           

            # the payment means a Admin is trying to subscribe
            CurrentTenant  = rel8tenant_related_models.Client.objects.get(schema_name=meta_data['schema_name'])
            TenantSub = subscription_related_models.TenantSubscription.objects.get(
           id =meta_data.get('instanceID'))
            # tenant=CurrentTenant,
            # this means the payment was succesfful
            TenantSub.is_paid_succesfully=True
            # this would be false for now our periodic task will set it to true meaning th sub has ended
            TenantSub.is_end=False
            TenantSub.save()
            subscription_related_models.setTimer(meta_data.get('instanceID'),"organization",meta_data['schema_name'],CurrentTenant)
        if meta_data['forWhat'] == 'fund_a_project':
            support_project_incash =  extras_models.SupportProjectInCash.objects.get(id=meta_data['instanceID'])
            support_project_incash.is_paid=True 
            support_project_incash.save()
            "update project amount made"
            project = extras_models.FundAProject.objects.get(id=support_project_incash.project.id)
            project.amount_made =project.amount_made+  support_project_incash.amount
            project.save()


        if meta_data['forWhat'] == 'prospective_member_registration':
            member_id =meta_data['member_id']
            instanceID = meta_data['instanceID']
            amount_to_be_paid= meta_data['amount_to_be_paid']
            if connection.schema_name == 'man':
                prospective_member = ManProspectiveMemberProfile.objects.get(id=instanceID)
                prospective_member.has_paid=True
                prospective_member.amount=float(amount_to_be_paid)
                prospective_member.save()
                thread = threading.Thread(target=mymailing_task.send_activation_mail,args=[prospective_member.user.id,prospective_member.user.email,connection.schema_name])
                thread.start()
                thread.join()  
            else:
                prospective_member= generalProspectiveModels.ProspectiveMemberProfile.objects.get(id=instanceID)
                prospective_member.has_paid=True
                prospective_member.amount_paid=amount_to_be_paid
                prospective_member.save()

        return HttpResponse(status.HTTP_200_OK)





@csrf_exempt
def useWebhook(request,pk=None):
    "this receives Payload from paystack"
    data = json.loads(request.body)
    meta_data =data['data']['metadata']
    connection.set_schema(schema_name=meta_data['schema_name'])
    user = get_user_model().objects.get(id=meta_data['user_id'])

    if data.get('event') == 'charge.success':
        return webhookPayloadhandler(meta_data,user)



@csrf_exempt
def useFlutterWaveWebhook(request,pk=None):
    'this receives payload from flutter waVE'
    print(request.body)
    data = json.loads(request.body)
    forWhat,user_id,instanceID,schema_name = data.get('txRef').split('---')[1].split('--') 
    meta_data ={
        'forWhat':forWhat,
        'instanceID':instanceID,
        'schema_name':schema_name
    }
    connection.set_schema(schema_name=meta_data['schema_name'])
    user = get_user_model().objects.get(id=user_id)


    if data.get('status') == 'successful' or data.get('event') == 'charge.completed':
        return webhookPayloadhandler(meta_data,user)


