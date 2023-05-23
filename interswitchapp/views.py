from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from rest_framework_xml.renderers import XMLRenderer
from utils.custom_response import Success_response,interswitchResponseWithAmountMoreTHan0 
from rest_framework.response import Response
from . import serailzer
from rest_framework.parsers import BaseParser
from utils.custom_parsers import CustomTextXmlPaser
# Create your views here.
# read this docs -> https://sandbox.interswitchng.com/docbase/docs/paydirect/rest-service-api/customer-data-validation/


#password Password1$

class PaymentValidation(viewsets.ViewSet):
    # queryset = User.objects.all()
    # serializer_class = UserSerializer
    parser_classes = (CustomTextXmlPaser,)
    renderer_classes = (XMLRenderer,)


    def create(self, request, *args, **kwargs):
        print({'data recived':request.data})
        payment_serializer = serailzer.PaymentSerializer(data=request.data)
        payment_serializer.is_valid(raise_exception=True)
        payment_data= payment_serializer.save()
        return interswitchResponseWithAmountMoreTHan0(**payment_data)
    