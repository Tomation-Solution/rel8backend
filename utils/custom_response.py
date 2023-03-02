# NOTE this file houses a function that gives Me a well formated Response So Now
# i can update response in one place
from rest_framework.response import Response
from rest_framework import status

def Success_response(msg,data=None,status_code=status.HTTP_200_OK):
    "anytime this function is called it returns this particular dictionary or error response"

    return Response(data={
        **structure_responseDict(msg,status_code,success=True,data=data)
    },status=status_code)


def structure_responseDict(msg,status_code,success,data=None):
    "this just returns a structured dictionary which would be used across this app so we wont have to re-righting"


    return {
         "message":msg,
        "status_code":status_code,
        "data":data,
        "success":success
    }
    

def interswitchResponseWithAmountMoreTHan0(**kwargs):
    ''
    CustReference = kwargs.get('CustReference')
    FirstName = kwargs.get('first_name')
    email = kwargs.get('email')
    Phone = kwargs.get('phone')
    amount = kwargs.get('amount')
    ProductName = kwargs.get('for_what')
    ProductCode = kwargs.get('instance_id')
    data ={
    'CustomerInformationResponse':{
        "MerchantReference":'',
        'Customers':{
            'Customer':{
                'Status':0,
                'OrgShortName':kwargs.get('OrgShortName'),
                'CustReference':CustReference,
                'CustomerReferenceAlternate':'',
                'FirstName':FirstName,
                'LastName':'',
                'Email':email,
                'Phone':Phone,
                'ThirdPartyCode':'ThirdPartyCode',
                'Amount':amount,
                'PaymentItems':{
                    'Item':{
                        'ProductName':ProductName,
                         'ProductCode':ProductCode,
                         'Quantity':1,
                         'Price':amount,
                         'Subtotal':amount,
                         'Tax':0,
                         'Total':amount
                    }
                }
            }   
        }
    }
}

    return Response(data=data,status=status.HTTP_200_OK)
# <CustomerInformationResponse>
#     <MerchantReference>639</MerchantReference>
#     <Customers>
#         <Customer>
#             <Status>0</Status>
#             <CustReference>23470</CustReference>
#             <CustomerReferenceAlternate></CustomerReferenceAlternate>
#             <FirstName>test test</FirstName>
#             <LastName></LastName>
#             <Email>tester@gmail.com</Email>
#             <Phone></Phone>
#             <ThirdPartyCode></ThirdPartyCode>
#             <Amount>234078</Amount>
#             <PaymentItems>
#                 <Item>
#                     <ProductName>PayAtBank</ProductName>
#                     <ProductCode>01</ProductCode>
#                     <Quantity>1</Quantity>
#                     <Price>234078</Price>
#                     <Subtotal>234078</Subtotal>
#                     <Tax>0</Tax>
#                     <Total>234078</Total>
#                 </Item>
#             </PaymentItems>
#         </Customer>
#     </Customers>
# </CustomerInformationResponse>