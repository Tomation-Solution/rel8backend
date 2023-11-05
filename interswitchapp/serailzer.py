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
def generate_interswitch_error(
MerchantReference:str,
CustReference:str,
Amount:int,
productname='',
productcode='',
error='',
Status=1
                               ):


    return {
    'MerchantReference':MerchantReference,
    'Customers':{
        'Customer':{
    'Status':Status,
    'CustReference':CustReference,
    'FirstName':'Null',
    'Email':'Null',
    'LastName':'Null',
    'Phone':'Null',
    'Amount':Amount,
    # 'error':error,
    'PaymentItems':{
        'Item':{
            'ProductName':productname,
            'ProductCode':productcode,
            'Quantity':'1',
            'Price':Amount,
            'Tax':'0',
            'Total':Amount,
            'Subtotal':Amount,
        }
    }
    }
    }}
    # return {
    # 'CustomerInformationResponse':{
    # 'MerchantReference':MerchantReference,
    # 'Customers':{
    #     'Customer':{
    # 'Status':1,
    # 'CustReference':CustReference,
    # 'CustomerReferenceAlternate':'',
    # 'FirstName':'',
    # 'Email':'',
    # 'LastName':'',
    # 'Phone':'',
    # 'ThirdPartyCode':'',
    # 'Amount':Amount,
    # 'Phone':'',
    # 'error':error,
    # 'PaymentItems':{
    #     'Item':{
    #         'ProductName':productname,
    #         'ProductCode':productcode,
    #         'Quantity':'1',
    #         'Price':Amount,
    #         'Subtotal':'',
    #         'Tax':'',
    #         'Total':Amount,
    #     }
    # }
    # }
    # }}}

	
"""
prospective_member_registration
due
event_payment
fund_a_project
"""
payload = {
    '1':'prospective_member_registration-man',
    '2':'due-man',
    '3':'event_payment-man',
    # '04':'fund_a_project-man',

    '5':'prospective_member_registration-nimn',
    '6':'due-nimn',
    '7':'event_payment-nimn',

    '8':'prospective_member_registration-migos',
    '9':'due-migos',
    '10':'event_payment-migos',

    # '08':'fund_a_project-nimn',
}
class PaymentSerializer(serializers.Serializer):
    MerchantReference = serializers.CharField(required=False,allow_null=True)
    CustReference =serializers.CharField(required=False,allow_null=True)
    PaymentItemCode= serializers.CharField(required=False,allow_null=True)

    """
    	Amount to be paid, NB: You must return amount has 0,
          when customers can pay for any amount
    """
    def validate(self, attrs):
        # schema_name = attrs.get('LastName',' ')
        CustReference = attrs.get('CustReference','0')
        MerchantReference = attrs.get('MerchantReference',0)


        error = generate_interswitch_error(
        MerchantReference=MerchantReference,CustReference='',
        Amount=0.00,error='cant find PaymentItemCode')
        if not attrs.get('PaymentItemCode','01-1') or not CustReference:
            raise PaymentError(error)
        if MerchantReference !='8269':
            raise PaymentError(error)
        item_id = attrs.get('PaymentItemCode',None)




        ForWhat = 'due'
        schema_name = 'nimn'


        request=''

        if item_id is None:
            raise PaymentError(error)
        # member id number
        # CustReference = attrs.get('CustReference',' ')
        # ForWhat = attrs.get('FirstName','')
        if not rel8tenant_related_models.Client.objects.filter(schema_name=schema_name).exists():
            error = generate_interswitch_error(
                MerchantReference=MerchantReference,CustReference=CustReference,
                Amount=0.00,error='schema does not exits')
            print('schema- dont exist')
            raise PaymentError(error)
        # set the schema to the particular tenat we want to deal with
        connection.set_schema(schema_name=schema_name)
        
        if not user_related_models.Memeber.objects.filter(id=CustReference).exists():
            "check if a member exits"
            error = generate_interswitch_error(
                MerchantReference=MerchantReference,CustReference=CustReference,
                Amount=0.00,error='members does not exits')
            print('members does not exits')
            raise PaymentError(error)
        if not (ForWhat.lower() in ['due','event_payment','fund_a_project']):
            print('forhwat')
            error = generate_interswitch_error(
                MerchantReference=MerchantReference,CustReference=CustReference,
                Amount=0.00,error='the type is not due')
            # error = generate_interswitch_error(merchant_reference,CustReference,0.00,
            # "must include at least one of this option.. 'due','event_payment','fund_a_project'")
            raise PaymentError(error)

        return super().validate(attrs)
    

    def create(self, validated_data):
        MerchantReference = validated_data.get('MerchantReference')

        item_id = validated_data.get('PaymentItemCode',None)
        CustReference = validated_data.get('CustReference','')
        member =user_related_models.Memeber.objects.get(id=CustReference)
        # PaymentItemCode= validated_data.get('PaymentItemCode',-1)

        forWhat ='due'
        # shortname= payload[PaymentItemCode].split('-')
        instance=''
        merchant_reference =item_id
        productName = ''
        if forWhat=="due":
            print({'forwhj':forWhat})
            due_users = due_models.Due_User.objects.all()
            if not due_users.filter(user=member.user,item_code=item_id,).exists():
                error = generate_interswitch_error(MerchantReference,
                                                    CustReference,0.00,
                                                    'Due Doesnt Exist',)
                print({'exist':'due does not exist'})
                raise PaymentError(error)
                    
            # if  due_users.filter(user=member.user,id=item_id,is_paid=True).exists():
            #     error = generate_interswitch_error(
            #     MerchantReference=MerchantReference,CustReference=CustReference,
            #     Amount=0.00)
            #     print({'exist':'due does not exist'})

            #     raise PaymentError(error)
            due_user = due_models.Due_User.objects.get(user=member.user,item_code=item_id)
            productName = due_user.due.Name
            # if due_user.is_paid == True:
            #     error = generate_interswitch_error(
            #     MerchantReference=MerchantReference,CustReference=CustReference,
            #     Amount=due_user.amount,Status=0)
            #     print({'exist':'has already paid for this due so we would return error but the status code should be 0'})
            #     raise PaymentError(error)    

            instance = due_user.due
            return   {
    'MerchantReference':MerchantReference,
    'Customers':{
        'Customer':{
    'Status':0,
    'CustReference':CustReference,
    'FirstName':member.full_name,
    'Email':member.user.email,
    'LastName':member.full_name,
    'Phone':member.telephone_number,
    # 'ThirdPartyCode':'',
    'Amount':int(instance.amount),
    # 'Phone':'',
    'PaymentItems':{
        'Item':{
            'ProductName':productName,
            'ProductCode':validated_data.get('PaymentItemCode',''),
            'Quantity':'1',
            'Price':int(instance.amount),
            # 'Subtotal':'',
            'Tax':0,
            'Total':int(instance.amount),
            'Subtotal':int(instance.amount),

        }
    }
    }
    }}
           
       
        error = generate_interswitch_error(
        MerchantReference=item_id,CustReference=CustReference,
        Amount=0.00)
        print({'exist':'Not due'})
        raise PaymentError(error)