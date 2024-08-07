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
from rest_framework.views import APIView
from rest_framework import status
from django.db import transaction
# pagination.py
from rest_framework.pagination import PageNumberPagination

class EventsResultPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page'
    max_page_size = 100


class UnauthorizedEventView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk=None, *args, **kwargs):
        """
        Handle GET requests. If a PK is provided, retrieve a single event. 
        Otherwise, list all events with pagination.
        """
        if pk:
            # Get event by PK
            event = get_object_or_404(models.Event, pk=pk)
            serializer = serializers.UnauthorizedEventSerializer(event, context={'request': request})
            return custom_response.Success_response(msg="success", data=serializer.data, status_code=status.HTTP_200_OK)
        else:
            # List all events with pagination
            all_events = models.Event.objects.all().order_by('-startDate')
            paginator = EventsResultPagination()
            paginated_events = paginator.paginate_queryset(all_events, request)
            serializer = serializers.UnauthorizedEventSerializer(paginated_events, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)

class EventViewSet(viewsets.ViewSet):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    permission_classes = [permissions.IsAuthenticated,custom_permission.IsAdminOrSuperAdmin,custom_permission.Normal_Admin_Must_BelongToACHapter]
    parser_classes = (NestedMultipartParser,FormParser,)
    filterset_class = custom_filter.EventLookUp

    def partial_update(self, request, pk=None):
        try:
            instance = models.Event.objects.get(id=pk)
        except models.Event.DoesNotExist:
            raise CustomError(message="Event is not available", status_code=404)

        serializer = self.serializer_class(instance, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return custom_response.Success_response(msg="Success", data=serializer.data, status_code=status.HTTP_200_OK)
        raise CustomError(message="Failed to update", status_code=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request, pk):
        try:
            instance = models.Event.objects.get(id=pk)
        except models.Event.DoesNotExist:
            raise CustomError(message="Event is not available", status_code=404)

        instance.delete()
        return custom_response.Success_response(msg='Deleted',data=pk,status_code=status.HTTP_204_NO_CONTENT)
    
    def list(self, request, *args, **kwargs):
        'this code let chapter see thier news'
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
        return custom_response.Success_response(msg='Event created successfully',data=clean_data.data,status_code=status.HTTP_201_CREATED)

    def get_queryset(self):
        "we getting the query set but if the person choose is_chapters we get the chapter data"
        is_chapter = self.request.query_params.get('is_chapter',None)
        user_chapter = self.request.user.chapter
        data = self.queryset.all()
        if is_chapter:
            return self.queryset.filter(chapters=user_chapter)
        return self.queryset.filter(chapters=None)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def list_of_register_members(self, request, format=None):
        event_id = request.query_params.get('event_id', None)
        if event_id is None:
            raise CustomError({'error': 'Event was not provided'})
        
        with transaction.atomic():

            # Filter EventDue_User instances by event_id and retrieve member IDs
            members = models.EventDue_User.objects.filter(event__id=event_id).values_list('user__memeber', flat=True)

            # Filter Member instances by the retrieved member IDs
            list_of_member_instance = user_related_models.Memeber.objects.filter(id__in=members)

            # Serialize the members to get only name and email
            data = [{'name': member.name, 'email': member.user.email} for member in list_of_member_instance]

            return custom_response.Success_response(msg='Success', data=data, status_code=200)

        # models.EventDue_User.objects.filter
    @action(detail=False,methods=['get'],permission_classes=[custom_permission.IsAdminOrSuperAdmin])
    def view_member_attendees(self,request,*args,**kwargs):
        event_id =  request.query_params.get('event_id',None)

        if not event_id:
            raise CustomError(message="Required event_id query", status_code=400)

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
    
    @action(detail=False,methods=['post'],permission_classes=[permissions.IsAuthenticated])
    def register_for_free_event(self,request,format =None):
        """
        this only works for free event
            first we check it the event exist and it is not paid
            then we register the user
        """

        serializer = serializers.RegiterForFreeEvent(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return  custom_response.Success_response(msg="Event Registration Successful")

    
    @action(detail=False,methods=['post'],permission_classes=[permissions.AllowAny])
    def public_event_registeration(self,request,format =None):

        serializer = serializers.PublicEventRegisterationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return  custom_response.Success_response(msg="Event Registration Successful", status_code=201)

    @action(detail=False,methods=['get'],permission_classes=[permissions.AllowAny])
    def public_attendees_list(self,request,format =None):
        event_id = request.query_params.get('event_id')
        public_events = models.PublicEvent.objects.filter(event_id=event_id)
        serializer = serializers.PublicEventSerializer(public_events, many=True)
        return  custom_response.Success_response(msg="Sucess", data=serializer.data, status_code=201)
    
    @action(detail=False,methods=['get'],permission_classes = [permissions.IsAuthenticated,custom_permission.IsMember])
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