from django.urls import reverse
from utils.custom_exceptions import CustomError
from utils.custom_response import Success_response
from rest_framework import status,authentication,permissions
from rest_framework.decorators import api_view,permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
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
    'Authorization': 'Bearer '+PAYSTACK_SECRET,
    'Content-Type' : 'application/json',
    'Accept': 'application/json',
    }
    try:
        resp = requests.get(url,headers=headers)
    except requests.ConnectionError:
        raise CustomError({"error":"Nework Error"}) 

    if resp.json()['data']['status'] == 'success':
        return Success_response(msg="Recived the Request Succefully",)
    raise CustomError({"error":"Something Went Wrong Try Again"})

 
class InitPaymentTran(APIView):
    "this is were the members pay for stuff read the code weel to get a hag of it"
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes=[
        permissions.IsAuthenticated,
        custom_permissions.IsMemberOrProspectiveMember]

    def post(self, request, forWhat="due",pk=None):
        

        """
        forWhat can be  = due,event,deactivating_due
        """
        if request.user.user_type== 'members':
            if(not user_model.Memeber.objects.all().filter(user=request.user).exists()):
                raise CustomError({"error":'member doest not exist'})

        

        schema_name = request.tenant.schema_name
        client_tenant = rel8tenant_related_models.Client.objects.get(schema_name=schema_name)
        
        # this is checking if the user has pluged his paystack account 
        if client_tenant.paystack_secret == 'null' or client_tenant.paystack_publickey == 'null':
            raise CustomError({'error':'Paystack not active please reach out to the developer'})
        PAYSTACK_SECRET = client_tenant.paystack_secret
        instance =None
            # Paystack intialization Url
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
                    raise CustomError({'error':'Please hold for admin to process your info you have paid already'})

        if forWhat=="due":
            # let get the id of due_user
            # let check if this user actually have due_user
            due_users = models.Due_User.objects.all()
            if not due_users.filter(user=request.user,id=pk,).exists():raise CustomError({"error":"Due Doesnt Exist"})
            if  due_users.filter(user=request.user,id=pk,is_paid=True).exists():raise CustomError({"error":"you have paid for this due already"})
            instance = models.Due_User.objects.get(user=request.user,id=pk)
            amount_to_be_paid = instance.amount

        if forWhat =='deactivating_due':
            deactivating_due = models.DeactivatingDue_User.objects.all()
            if not deactivating_due.filter(user=request.user,id=pk,).exists():raise CustomError({"error":"Due Deactivating Due Exist"})
            if  deactivating_due.filter(user=request.user,id=pk,is_paid=True).exists():raise CustomError({"error":"you have paid for this due already"})
            
            instance = models.DeactivatingDue_User.objects.get(user=request.user,id=pk)
            amount_to_be_paid = instance.amount

        if forWhat =='event_payment':
            event_users = event_models.EventDue_User.objects.all()
            events = event_models.Event.objects.all()
            if not events.filter(id=pk,).exists():raise CustomError({"error":"Event Does Not Exist maybe it was deleted"})
            event = event_models.Event.objects.get(id=pk )
            if event_users.filter(user=request.user,event=event,is_paid=True).exists():raise CustomError({"error":"Hello you have paid for this event"})
            
            instance,_ = event_models.EventDue_User.objects.get_or_create(
                user=request.user,event=event,amount=event.amount,)
            amount_to_be_paid = instance.amount
            pk = instance.id#we did this cause we accessing the eventdue_user
        if forWhat =='fund_a_project':
            'since this is a donation there is no fix price we get it from the query param'
            amount  = request.query_params.get('donated_amount',None)
            if amount is None:
                raise CustomError({'error':'Please amount it missing'})
            "here we check it the"
            try:
                amount = int(amount)
            except ValueError:
                raise CustomError({'error':'amount must be number '})
            fundAProject = extras_models.FundAProject.objects.get(id=pk)
            instance,_ = extras_models.SupportProjectInCash.objects.get_or_create(
                member = request.user.memeber,
                project=fundAProject,
                
            )
            fundAProject.amount = amount
            instance.save()
            amount_to_be_paid=instance.amount
        # if 
        if(instance==None):raise CustomError({"error":"Something went wrong"})
        if request.user.user_type== 'members':
            member = user_model.Memeber.objects.get(user=request.user)
        if request.user.user_type== 'prospective_members':
            if connection.schema_name == 'man':
                member =ManProspectiveMemberProfile.objects.get(user=request.user)
            else:
                member = generalProspectiveModels.ProspectiveMemberProfile.objects.get(user=request.user)
        
        url = 'https://api.paystack.co/transaction/initialize/'
        headers = {
            'Authorization': f'Bearer {PAYSTACK_SECRET}',
            'Content-Type' : 'application/json',
            'Accept': 'application/json',}
        body = {
            "email": request.user.email,
            "amount": convert_naira_to_kobo(amount_to_be_paid),
            "metadata":{
                "instanceID":pk,
                'member_id':member.id,
                "user_id":request.user.id,
                "forWhat":forWhat,
                'schema_name':request.tenant.schema_name,
                'user_type':request.user.user_type,
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
        
            # we create a transaction history upload nessary data by this time is_successfull will always be false
            # we put in paystack refrence in the current due the user wants to pay  data['data']['reference']
            # we use wehook to confirm the payment
            instance.paystack_key= data['data']['reference']
            instance.save()

            return Success_response(msg='Success',data=data)

        raise CustomError(message='Some Error Occured Please Try Again',status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

@csrf_exempt
def useWebhook(request,pk=None):
    "this receives Payload from paystack"
    data = json.loads(request.body)
    meta_data =data['data']['metadata']
    connection.set_schema(schema_name=meta_data['schema_name'])
    user = get_user_model().objects.get(id=meta_data['user_id'])

    if data.get('event') == 'charge.success':
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
                mymailing_task.send_activation_mail.delay(prospective_member.user.id,prospective_member.user.email)
            else:
                prospective_member= generalProspectiveModels.ProspectiveMemberProfile.objects.get(id=instanceID)
                prospective_member.has_paid=True
                prospective_member.amount_paid=amount_to_be_paid
                prospective_member.save()

        return HttpResponse(status.HTTP_200_OK)
