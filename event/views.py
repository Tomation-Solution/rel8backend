from django.shortcuts import render
from rest_framework import viewsets,permissions,status,mixins

from utils.custom_exceptions import CustomError
from . import models,serializers,filter as custom_filter
from utils import permissions as custom_permission
from utils import custom_response
from rest_framework.decorators import action
from account.models import user as user_related_models
from rest_framework.parsers import FormParser
from utils.custom_parsers import NestedMultipartParser
from account.serializers import user as user_related_serializer
from django.shortcuts import get_object_or_404

class EventViewSet(viewsets.ViewSet):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    permission_classes = [permissions.IsAuthenticated,custom_permission.IsAdminOrSuperAdmin,custom_permission.Normal_Admin_Must_BelongToACHapter]
    parser_classes = (NestedMultipartParser,FormParser,)
    filterset_class = custom_filter.EventLookUp
    def destroy(self,request,pk=None):
        instance = self.queryset.get(id=pk)
        instance.delete()
        return custom_response.Success_response(msg='Deleted',data=pk,status_code=status.HTTP_204_NO_CONTENT)
    def list(self, request, *args, **kwargs):
        'this code let chapter see thier news '
        all_events = self.queryset
        if self.request.query_params.get('is_chapter',None):
            "get event for only chapters"
            all_events=all_events.filter(chapters = request.user.chapter)
        else:
            'get global event'
            all_events=all_events.filter(chapters =None)
        clean_data = self.serializer_class(all_events,many=True,context={'request':request})
        return custom_response.Success_response(msg='success',data=clean_data.data,status_code=status.HTTP_200_OK)
          
    def create(self,request,format=None):
        'create event'
        serialize =  self.serializer_class(data=request.data,context={"request":request})
        serialize.is_valid(raise_exception=True)
        instance = serialize.save()
        duesObject = models.Event.objects.get(id=instance.id)
        clean_data = self.serializer_class(duesObject,many=False,context={'request':request})
        return custom_response.Success_response(msg='Due created successfully',data=clean_data.data,status_code=status.HTTP_201_CREATED)

    def get_queryset(self):
        "we getting the query set but if the person choose is_chapters we get the chapter data"
        is_chapter = self.request.query_params.get('is_chapter',None)
        user_chapter = self.request.user.chapter
        data = self.queryset.all()
        if is_chapter:
            return self.queryset.filter(chapters=user_chapter)
        return self.queryset.filter(chapters=None)

    @action(detail=False,methods=['post'],permission_classes=[permissions.IsAuthenticated,])
    def list_of_register_members(self,request,format=None):
        event_id= request.data.get('event_id',None)
        if event_id is None:raise CustomError({'error':'Event was not provided'})
        # event = models.Event.objects.get(id=event_id)
        
    
        members = models.EventDue_User.objects.filter(event__id=event_id).values('user__memeber')
        def filter_member(member_id):return member_id.get('user__memeber')
        list_of_member_id = list(map(filter_member,members))
        
        list_of_member_instance = user_related_models.Memeber.objects.filter(id__in=list_of_member_id )
        data = user_related_serializer.MemberSerializer(list_of_member_instance,many=True)
        return custom_response.Success_response('Succes',data=data.data,status_code=status.HTTP_200_OK)
        # models.EventDue_User.objects.filter
    @action(detail=False,methods=['post'],permission_classes=[permissions.IsAuthenticated,])
    def view_attendies(self,request,*args,**kwargs):
        event_id =  request.data.get('event_id',None)
        event = get_object_or_404(models.Event,id=event_id)
        event_due_user = models.EventDue_User.objects.filter(event=event)
        clean_data = serializers.RegisteredEventMembersSerializerCleaner(instance=event_due_user,many=True)
        
        return custom_response.Success_response('Success',data=clean_data.data,status_code=status.HTTP_200_OK)

    @action(detail=False,methods=['post'],permission_classes=[permissions.IsAuthenticated,custom_permission.IsAdminOrSuperAdmin])
    def activate_event(self,request,format =None):
        serialize = serializers.AdminManageEventActiveStatus(data=request.data,context={"request":request})
        serialize.is_valid(raise_exception=True)
        data = serialize.save()
        clean_data = serializers.EventSerializer(data,many=False,context={"request":request})
         
        return custom_response.Success_response(msg='Active Status Updated.',data=clean_data.data,status_code=status.HTTP_200_OK)
    
    @action(detail=False,methods=['post'],permission_classes=[permissions.IsAuthenticated,custom_permission.IsMember])
    def register_for_free_event(self,request,format =None):
        """
        this only works for free event
            first we check it the event exist and it is not paid
            then we register the user
        """

        serializer = serializers.RegiterForFreeEvent(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return  custom_response.Success_response(msg="Registration Successful")


    """    @action(detail=False,methods=['get'],permission_classes = [permissions.IsAuthenticated,custom_permission.IsMember])
        def get_events(self,request,format=None):
            # models.Event.objects.all().filter(id=instance.id).values()
            # print(self.request.query_params.)
            # is_for_excos
            # is_commitee 
            member  = user_related_models.Memeber.objects.get(user=request.user)
            # is_exco = member.is_exco
            # is_commitee = member.commiteegroup_set.all()
            commitee_id=None
            all_events = self.queryset.filter()
            # is_for_excos=is_exco
            get_exco_event = self.request.query_params.get('is_exco',False)
            if get_exco_event:
                "get exco events"
                if member.is_exco==False:
                    'if this user is not a exco tell he cant see exco stuff'
                    raise CustomError({'error':'you are not an exco'})
                # this means the person can see exco stuff
                all_events = self.queryset.filter(is_for_excos=True)

            if self.request.query_params.get('is_chapter',None):
                "get event for my chapter"
                all_events=all_events.filter(chapters = request.user.chapter)
            else:
                "get event for all global not chapter specific"
                all_events=all_events.filter(chapters =None)
            
            if self.request.query_params.get('commitee_id',None):
                "this would filter by commitee id"
                # check it this member belongs to the committee
                if member.commiteegroup_set.all().filter(members__id=member.id).exists():
                    commitee_id=self.request.query_params.get('commitee_id')
                    all_events = self.queryset.filter(commitee=commitee_id)

            clean_data = self.serializer_class(all_events,many=True,context={'request':request})
            return custom_response.Success_response(msg='success',data=clean_data.data,status_code=status.HTTP_200_OK)

    """  
    @action(detail=False,methods=['get'],permission_classes = [permissions.IsAuthenticated,custom_permission.IsMember],

    )
    def get_events(self,request,format=None):
        
        filter_set = custom_filter.EventLookUp(request.query_params,queryset=self.get_queryset().order_by('-startDate'))
        # print({'filter_set':filter_set.qs})
        # queryset = filter_set.filter_queryset(self.get_queryset())
        clean_data = self.serializer_class(filter_set.qs,many=True,context={'request':request})
        return custom_response.Success_response(msg='success',data=clean_data.data,status_code=status.HTTP_200_OK)

class RescheduleEventRequestViewSet( mixins.ListModelMixin,mixins.CreateModelMixin,viewsets.GenericViewSet):
    permission_classes= [permissions.IsAuthenticated,custom_permission.IsMember]
    serializer_class = serializers.RescheduleEventRequestSerializer
    queryset= models.RescheduleEventRequest.objects.all()
    filterset_class= custom_filter.RescheduleEventRequestFilter


    def list(self, request, *args, **kwargs):
        param = request.query_params.get('event_id',0)
        data =  models.RescheduleEventRequest.objects.filter(event__id=param)
        clean_data = self.serializer_class(data,many=True)
        return custom_response.Success_response('Success',data=clean_data.data)