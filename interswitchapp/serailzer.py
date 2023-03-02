from rest_framework import serializers
from django.db import connection
from Rel8Tenant import models as rel8tenant_related_models
from rest_framework.response import Response
from rest_framework import status
from utils.custom_exceptions import CustomError,PaymentError
from account.models import user as user_related_models
from Dueapp import models as  due_models

# <CustomerInformationRequest>
#     <ServiceUsername></ServiceUsername>
#     <ServicePassword></ServicePassword>
#     <MerchantReference>6405</MerchantReference>
#     <CustReference>111111117</CustReference>
#     <PaymentItemCode>01</PaymentItemCode>
#     <ThirdPartyCode></ThirdPartyCode>
# </CustomerInformationRequest>


# data = {
#     'CustomerInformationResponse':{
#     'MerchantReference':2,
#     'Customers':{
#         'Customer':{
#     'Status':0,
#     'CustReference':111111117,
#     'CustomerReferenceAlternate':'',
#     'ThirdPartyCode':'',
#     'Amount':0.00}
#     }}}
def generate_interswitch_error(MerchantReference:str,CustReference:str,Amount:int,msg):

    return {
    'CustomerInformationResponse':{
    'MerchantReference':MerchantReference,
    'Customers':{
        'Customer':{
    'Status':1,
    'CustReference':CustReference,
    'CustomerReferenceAlternate':'','ThirdPartyCode':'',
    'Amount':Amount,
    'ErrorMessage':msg
    }
    }}}

class PaymentSerializer(serializers.Serializer):
    MerchantReference = serializers.CharField(required=False)
    PaymentItemCode= serializers.IntegerField(required=False)
    OrgShortName =  serializers.CharField(required=False)
    ForWhat = serializers.CharField(required=False)
    CustReference =serializers.IntegerField(required=False)

    """
    	Amount to be paid, NB: You must return amount has 0,
          when customers can pay for any amount
    """
    def validate(self, attrs):
        schema_name = attrs.get('OrgShortName',' ')
        merchant_reference = attrs.get('merchant_reference',' ')
        # member id number
        CustReference = attrs.get('CustReference',' ')
        ForWhat = attrs.get('ForWhat','')
        if not rel8tenant_related_models.Client.objects.filter(schema_name=schema_name).exists():
            error = generate_interswitch_error(merchant_reference,CustReference,0.00,'incorrect OrgShortName')
            raise PaymentError(error)
        # set the schema to the particular tenat we want to deal with
        connection.set_schema(schema_name=schema_name)
        
        if not user_related_models.Memeber.objects.filter(id=CustReference).exists():
            "check if a member exits"
            error = generate_interswitch_error(merchant_reference,CustReference,0.00,'Member does not exist')
            raise PaymentError(error)
        if not (ForWhat.lower() in ['due','event_payment','fund_a_project']):
            error = generate_interswitch_error(merchant_reference,CustReference,0.00,
            "must include at least one of this option.. 'due','event_payment','fund_a_project'")
            raise PaymentError(error)

        return super().validate(attrs)
    

    def create(self, validated_data):
        merchant_reference = validated_data.get('merchant_reference',' ')
        forWhat = validated_data.get('ForWhat',)
        CustReference = validated_data.get('CustReference','')
        member =user_related_models.Memeber.objects.get(id=CustReference)
        item_id = validated_data.get('PaymentItemCode',-1)

        
        if forWhat=="due":
            print({'forwhj':forWhat})
            due_users = due_models.Due_User.objects.all()
            if not due_users.filter(user=member.user,id=item_id,).exists():
                error = generate_interswitch_error(merchant_reference,
                                                    CustReference,0.00,
                                                    'Due Doesnt Exist')
                raise PaymentError(error)
                    
            if  due_users.filter(user=member.user,id=item_id,is_paid=True).exists():
                error = generate_interswitch_error(merchant_reference,CustReference,0.00,
                                                    'you have paid for this due already')
                raise PaymentError(error)
            instance = due_models.Due_User.objects.get(user=member.user,id=item_id)

        
            return {
            'CustReference':CustReference,
            'first_name':member.full_name,
            'email':member.user.email,
            'phone':'',
            'amount':instance.amount,
            'for_what':forWhat,
            'instance_id':instance.id,
            'OrgShortName':validated_data.get('OrgShortName'),
            }
        
        error = generate_interswitch_error(merchant_reference,
                    CustReference,0.00,
                    'Please Check the api parameters well you might be missing a para')
        raise PaymentError(error)