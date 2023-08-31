from django.shortcuts import render
from rest_framework import viewsets,permissions
from . import serializer,models
from utils.pagination import CustomPagination
from utils import permissions as custom_permission
from rest_framework.decorators import action
from utils.custom_response import Success_response





class MemberLastestUpdatesViewSet(viewsets.ModelViewSet):
    serializer_class =  serializer.LastestUpdatesMemberSerializer
    queryset = models.LastestUpdates.objects.all()
    permission_classes = [permissions.IsAuthenticated,custom_permission.IsMember]
    page_size = 15



class AdminLastestUpdatesViewSet(viewsets.ModelViewSet):
    serializer_class =  serializer.LastestUpdatesAdminSerializer
    queryset = models.LastestUpdates.objects.all()
    permission_classes = [permissions.IsAuthenticated,custom_permission.IsAdminOrSuperAdmin]
    page_size = 15


    @action(methods=['post'],detail=False)
    def send_push_individual_nofication(self,request):
        print({'data':request.data})
        serial = serializer.IndividaulNotification(data=request.data,context={'request':request})
        serial.is_valid(raise_exception=True)
        serial.save()


        return Success_response('Sent')
    @action(methods=['post'],detail=False)
    def send_notification_by_topic(self,request):
        # +'--exco'
        serial =serializer.NotificationByTopicSerializer(data=request.data)
        serial.is_valid(raise_exception=True)
        serial.save()
        return Success_response('Sent')
