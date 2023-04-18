from django.shortcuts import render
from rest_framework import viewsets,permissions,status
from utils import permissions as custom_permission
from . import models,filter as custom_filter
from utils import custom_response
from utils.custom_exceptions import CustomError
from . import serializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from utils import custom_response,custom_parsers
from rest_framework.parsers import  FormParser


class MeetingMemberViewSet(viewsets.ViewSet):
    permission_classes = [ permissions.IsAuthenticated,custom_permission.IsMember,custom_permission.Isfinancial]
    queryset =models.Meeting.objects.all()


    def get_queryset(self):
        "we getting the query set but if the person choose is_chapter we get the chapter data"
        # is_chapter = self.request.query_params.get('is_chapter',None)
        # user_chapter = self.request.user.chapter
        # if is_chapter:
        #     return self.queryset.filter(chapters=user_chapter)
        return self.queryset.filter()
    def list(self,request,format=None):

        filter_set = custom_filter.MeetingFitlter(request.query_params,queryset=self.get_queryset().order_by('-event_date'))

        clean_data = serializer.MeetingSerializer(filter_set.qs,many=True,context={'user':request.user})
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

    @action(methods=['post'],detail=False )
    def non_meeting_attenders(self,request,*args,**kwargs):
        meeting_id = request.data.get('meeting',None)
        meeting = get_object_or_404(models.Meeting,id=meeting_id)
        meeting_appolgies =models.MeetingApology.objects.filter(meeting=meeting)
        serialized = serializer.NonattendersMeetingMembersSerializer(instance=meeting_appolgies,many=True)


        return custom_response.Success_response(msg='Success',data=serialized.data,status_code=status.HTTP_200_OK)
        
    @action(methods=['post'],detail=False)
    def appologise_for_not_attending(self,request,*args,**kwargs):
        meeting_id = request.data.get('meeting',None)
        meeting = get_object_or_404(models.Meeting,id=meeting_id)

        applogy = serializer.MeetingApologies(data=request.data,context={'user':request.user})
        applogy.is_valid(raise_exception=True)
        applogy.save()
        return custom_response.Success_response(msg='Appology Accepted',data=[],status_code=status.HTTP_201_CREATED)

class AdminManagesMeetingViewset(viewsets.ModelViewSet):
    permission_classes = [ permissions.IsAuthenticated,custom_permission.IsAdminOrSuperAdmin]
    queryset =models.Meeting.objects.all()
    serializer_class = serializer.AdminManageMeetingSerializer
    parser_classes =(custom_parsers.NestedMultipartParser,FormParser,)


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
