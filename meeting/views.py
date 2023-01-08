from django.shortcuts import render
from rest_framework import viewsets,permissions,status
from utils import permissions as custom_permission
from . import models,filter as custom_filter
from utils import custom_response
from utils.custom_exceptions import CustomError
from . import serializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


class MeetingMemberViewSet(viewsets.ViewSet):
    permission_classes = [ permissions.IsAuthenticated,custom_permission.IsMember]
    queryset =models.Meeting.objects.all()


    def get_queryset(self):
        "we getting the query set but if the person choose is_chapter we get the chapter data"
        is_chapter = self.request.query_params.get('is_chapter',None)
        user_chapter = self.request.user.chapter
        if is_chapter:
            return self.queryset.filter(chapters=user_chapter)
        return self.queryset.filter(chapters=None)
    def list(self,request,format=None):

        filter_set = custom_filter.MeetingFitlter(request.query_params,queryset=self.get_queryset())

        clean_data = serializer.MeetingSerializer(filter_set.qs,many=True)
        return custom_response.Success_response(msg='Success',data=clean_data.data,status_code=status.HTTP_200_OK)

    def create(self,request,*args,**kwargs):
        

        serialized=serializer.MeetingRegister(data=request.data,context={'user':request.user})
        serialized.is_valid(raise_exception=True)
        serialized.save()
        return custom_response.Success_response(msg='Registered',data=[],status_code=status.HTTP_201_CREATED)

    @action(methods=['post'],detail=False)
    def get_register_members(self,request,*args,**kwargs):
        meeting_id = request.data.get('meeting_id',None)

        meeting = get_object_or_404(models.Meeting,id=meeting_id)


        serilied = serializer.RegisteredMeetingMembersSerializer(meeting,many=False)
        return custom_response.Success_response(msg='Success',data=serilied.data,status_code=status.HTTP_200_OK)


class AdminManagesMeetingViewset(viewsets.ModelViewSet):
    permission_classes = [ permissions.IsAuthenticated,custom_permission.IsAdminOrSuperAdmin]
    queryset =models.Meeting.objects.all()
    serializer_class = serializer.AdminManageMeetingSerializer


    def get_queryset(self):
        'if it super user we dont filter by chapter if it is then we filter by chapter'
        user_chapter = self.request.user.chapter
        if self.request.user.user_type == 'admin':
            return self.queryset.filter(chapters=user_chapter)
        return self.queryset.filter(chapters=None)

    def list(self,request,format=None):

        filter_set = custom_filter.MeetingFitlter(request.query_params,queryset=self.get_queryset())

        clean_data = serializer.MeetingSerializer(filter_set.qs,many=True)
        return custom_response.Success_response(msg='Success',data=clean_data.data,status_code=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
