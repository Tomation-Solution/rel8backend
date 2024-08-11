import threading
import logging
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import ContactUsSerializer
from .task import send_contact_us_mail
from django.db import connection
from rest_framework.permissions import AllowAny
# Create your views here.


class TechnicalSuppportView(APIView):

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):        
        serializer = ContactUsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = {
            'sender_email': serializer.validated_data.get('sender_email'),
            'sender_name': serializer.validated_data.get('sender_name'),
            'schema_name': connection.schema_name,
            'message': serializer.validated_data.get('message')
        }

        logging.info(f"Received contact us request from {request.data.get('sender_email')} stated: {request.data.get('message')}")

        try:
            thread = threading.Thread(target=send_contact_us_mail,args=[data])
            thread.start()
            thread.join()
        except threading.ThreadError as e:
            logging.exception("Failed to start email sending thread")
            return Response({
                "message": "Failed to send contact us message."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        logging.info("Started contactus email sending thread...")

        return Response({
            "message": "Technical contact us message is on the way!",
        }, status=status.HTTP_201_CREATED)




class AdminSuppportView(APIView):

    def post(self, request):
        pass