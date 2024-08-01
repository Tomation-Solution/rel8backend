from rest_framework import serializers

from utils.custom_exceptions import CustomError
from . import models
from account.models import auth as auth_related_models
from account.models import user as user_related_models
from django.shortcuts import get_object_or_404
from mymailing import tasks as mailing_tasks

class RescheduleEventRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RescheduleEventRequest
        fields = '__all__'


class UnauthorizedEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Event
        fields = "__all__"


class EventSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    image =  serializers.ImageField(required=False)
    name =serializers.CharField()
    is_paid_event =serializers.BooleanField(required=True)
    re_occuring= serializers.BooleanField(required=True)# due_type Once  Re-occuring|
    is_virtual=serializers.BooleanField(required=True)
    # is_for_excos = serializers.BooleanField(required=True)#embers | excos
    commitee_id = serializers.IntegerField(required=False)
    exco_id = serializers.IntegerField(required=False)
    amount=  serializers.CharField(required=True)
    is_active = serializers.BooleanField()
    startDate =serializers.DateField(required=False)
    startTime = serializers.TimeField(required=False)
    # for is re-occuring there must be a startDate and endDate
    # endDate =models.DateField(null=True, blank=True)
    scheduletype = serializers.CharField(required=False)
    schedule = serializers.JSONField(required=False)
    'for only write only... we want to control the adress so only paid users can access it'
    address = serializers.CharField(write_only=True)
    event_access = serializers.SerializerMethodField()


    organiser_extra_info = serializers.CharField(required=False)
    organiser_name = serializers.CharField(required=False)
    event_extra_details = serializers.CharField(required=False)
    event_docs = serializers.FileField(required=False)
    organiserImage = serializers.ImageField(required=False)
    is_special = serializers.BooleanField(required=False)
    # for_chapters=serializers.BooleanField(default=False,)
    # def validate(self, attrs):
        
    #     return super().validate(attrs)
    # def get_address(self,event)
    def get_event_access(self,event):
        link=''
        has_paid=False
        requests = self.context.get('request')
        user = self.context.get('request').user

        if requests.user.user_type in ['admin','super_admin']:
            return {
                'link':event.address,
                'has_paid':True
            }
        else:
            "u have to be register before u see a event"
            if event.is_paid_event==False:
                if models.EventDue_User.objects.filter(user=user,event=event,is_paid=True).exists():
                    link=event.address
                    has_paid=True
                else:
                    "this just means user has not registered"
                    link =''
                    has_paid=False
            else:
                'this is a paid event and wee need to do some check'
                if  models.EventDue_User.objects.filter(user=user,event=event,is_paid=True).exists():
                    event_due_user = models.EventDue_User.objects.get(user=user,event=event)
                    has_paid= event_due_user.is_paid
                    link=event.address

                else:
                    'this this user has not tried to pay at all'
                    has_paid=False

            return {
                'has_paid':has_paid,
                'link':event.address
            }
    def create(self, validated_data):

        user = self.context.get('request').user
        # Super_admin
        commitee_id = validated_data.get("commitee_id",None)
        scheduletype = validated_data.get("scheduletype",None)
        schedule = validated_data.get("schedule",None)
        re_occuring = validated_data.get("re_occuring",None)
        exco_id = validated_data.get('exco_id',None)
        is_special = validated_data.pop('is_special',False)
        is_paid_event= validated_data.pop('is_paid_event',False)
        if(re_occuring==True):
            if scheduletype is None:
                raise CustomError({'scheduletype':'required'})
            if schedule is None:
                raise CustomError({'schedule':'required'})
        
        commitee =None
        if commitee_id:
            if user_related_models.CommiteeGroup.objects.filter(id=commitee_id).exists():
                commitee = user_related_models.CommiteeGroup.objects.get(id=commitee_id)
            else:
                raise serializers.ValidationError({"commitee_id":"commitee does not exist"})
        chapter = None
        if  user.user_type in ['admin']:
            chapter = auth_related_models.Chapters.objects.get(id=user.chapter.id)
        if user.user_type in ['super_admin']:
            'this means this person wants to create National Event he must be a super admin'
            chapter =None
            # if not user_related_models.Super_admin.objects.all().filter(user=user).exists():
            #     "if this user is not a super admin there is a problem he cant create a national event"
            #     raise CustomError({"error":"You can't Create A national Event"})
        exco =None
        if exco_id:
            "this means the user want to make this event for this type of exco"
            try:
                exco =get_object_or_404(user_related_models.ExcoRole,id=exco_id)
            except:
                raise CustomError({'error':'Exco Does not exist'})

        if is_special:
            "special event must be paid"
            if is_paid_event==False and is_special:raise CustomError({'error':'Special Event Must Be Paid'})

        event =  models.Event.objects.create(
            **validated_data,chapters=chapter,commitee=commitee,
            is_paid_event=is_paid_event,
            is_special=is_special,
        )

        event.exco=exco
        event.save()
        return event



class AdminManageEventActiveStatus(serializers.Serializer):
    switch_on =serializers.BooleanField()
    event_id = serializers.IntegerField()

    def validate(self, attrs):
        if attrs.get('event_id') is None:raise CustomError({'event_id':'Invalid event_id'})
        if not models.Event.objects.filter(id=attrs.get('event_id')).exists():
            raise CustomError({'event_id':'Invalid event_id'})
        return super().validate(attrs)


    def create(self, validated_data):
        'we would update the active status here'
        event_id = validated_data.get('event_id')
        switch_on = validated_data.get('switch_on')
        instance  = models.Event.objects.get(id=event_id)
        if switch_on:# if it tru then we activate the Event
            instance.is_active=True
        else:
            instance.is_active=False

        instance.save()
        return  instance

    def update(self, instance, validated_data):
        raise  CustomError({'error':'Not Available '})

class EventProxyAttendiesSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    email = serializers.EmailField()

class RegiterForFreeEvent(serializers.Serializer):
    event_id = serializers.IntegerField()
    proxy_participants = EventProxyAttendiesSerializer(many=True, required=False)

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request.user.is_authenticated else None

        proxy_participants = validated_data.get('proxy_participants', [])
        event_id = validated_data.get('event_id')
            

        try:
            event = models.Event.objects.get(id=event_id)
        except models.Event.DoesNotExist:
            raise CustomError({'error': 'Event Does Not Exist'})

        # Check if the event is paid
        if event.is_paid_event:
            raise CustomError({'error': 'You need to pay because this event is paid'})

        # Check if the user has already registered for the event (for authenticated users only)
        if user and models.EventDue_User.objects.filter(event=event, user=user).exists():
            raise CustomError({'error': 'You have already registered'})

        # Register the user for the event or set user to None if unauthenticated
        registration = models.EventDue_User.objects.create(
            user=user,
            event=event,
            amount=0.00,
            paystack_key="free_event",
            is_paid=True
        )

        # Handle proxy participants if provided
        if proxy_participants:
            event_proxy_attendies, created = models.EventProxyAttendies.objects.get_or_create(
                event_due_user=registration
            )
            event_proxy_attendies.participants = proxy_participants
            event_proxy_attendies.save()

            mailing_tasks.send_event_invitation_mail(
                user_id=user.id if user else None,
                event_id=event.id,
                event_proxy_attendies_id=event_proxy_attendies.id
            )

        return registration

class RegisteredEventMembersSerializerCleaner(serializers.ModelSerializer):
    proxy_participants = serializers.SerializerMethodField()
    member = serializers.SerializerMethodField()

    def get_member(self, instance: models.EventDue_User):
        # Handle cases where the user is None (for unauthenticated free event registrations)
        if instance.user is None:
            return {
                'full_name': 'Anonymous',
                'email': 'N/A',
                'member_id': None
            }

        # Fetch and return member details if the user exists
        try:
            member = user_related_models.Memeber.objects.get(user=instance.user)
            return {
                'full_name': member.full_name,
                'email': instance.user.email,
                'member_id': member.id
            }
        except user_related_models.Memeber.DoesNotExist:
            return {
                'full_name': 'Unknown',
                'email': instance.user.email if instance.user else 'N/A',
                'member_id': None
            }

    def get_proxy_participants(self, instance: models.EventDue_User):
        try:
            meeting_proxy_attendies = models.EventProxyAttendies.objects.get(event_due_user=instance)
            return meeting_proxy_attendies.participants
        except models.EventProxyAttendies.DoesNotExist:
            return []

    class Meta:
        model = models.EventDue_User
        fields = [
            'proxy_participants', 'member', 'id'
        ]