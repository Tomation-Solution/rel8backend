from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from rest_framework_xml.renderers import XMLRenderer
from utils.custom_response import Success_response,interswitchResponseWithAmountMoreTHan0 
from rest_framework.response import Response
from . import serailzer
from rest_framework.parsers import BaseParser
from utils.custom_parsers import CustomTextXmlPaser
from Dueapp import models as  due_models
from account.models import user as user_related_models
from django.db import connection
# Create your views here.
# read this docs -> https://sandbox.interswitchng.com/docbase/docs/paydirect/rest-service-api/customer-data-validation/


#password Password1$
class PaymentValidationXml(XMLRenderer):
    root_tag_name='CustomerInformationResponse'
    content_type ='text/xml'
    media_type ='text/xml'

class PaymentValidationResponseXml(XMLRenderer):
    root_tag_name='PaymentNotificationResponse'
    content_type ='text/xml'
    media_type ='text/xml'
    

class PaymentNotificationXml(XMLRenderer):
    root_tag_name='CustomerInformationResponse'
    content_type ='text/xml'
    media_type ='text/xml'

class PaymentValidation(viewsets.ViewSet):
    # queryset = User.objects.all()
    # serializer_class = UserSerializer
    parser_classes = (CustomTextXmlPaser,)
    renderer_classes = (PaymentValidationXml)


    def create(self, request, *args, **kwargs):
        print({'data recived':request.data})
        payment_serializer = serailzer.PaymentSerializer(data=request.data)
        payment_serializer.is_valid(raise_exception=True)
        payment_data= payment_serializer.save()
        return Response(data=payment_data,content_type="text/xml")
        # return interswitchResponseWithAmountMoreTHan0(**payment_data)

class PaymentNotification(viewsets.ViewSet):
    parser_classes = (CustomTextXmlPaser,)
    renderer_classes = (PaymentValidationResponseXml,)

    def create(self,request,*args,**kwargs):
        PaymentLogId = request.data.get('Payments').get('Payment').get('PaymentLogId')
        try:
            data = request.data
            IsReversal = request.data.get('Payments').get('Payment').get('IsReversal')
            # try:
            PaymentItemCode,item_id  = request.data.get('Payments').get('Payment').get('PaymentItems').get('PaymentItem').get('ItemCode','01-1').split('-') 
            CustReference  = request.data.get('Payments').get('Payment').get('CustReference') 
            ForWhat,schema_name = serailzer.payload[PaymentItemCode].split('-')
            connection.set_schema(schema_name=schema_name)
            member =user_related_models.Memeber.objects.get(id=CustReference)
            due= due_models.Due_User.objects.filter(user=member.user,id=item_id,).first()
            due.is_paid =True
            due.save()
            response = self.response_gen(PaymentLogId,0)

        except:

            response = self.response_gen(PaymentLogId,1)
        return Response(data=response,content_type="text/xml") 


    def response_gen(self,paymentLogID,Status):return{
            'Payments':{
                    'Payment':{
                        'PaymentLogId':paymentLogID,
                        'Status':Status
                    }
                }
        }