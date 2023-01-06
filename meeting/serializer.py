from rest_framework import serializers
from . import models
from utils.custom_exceptions import CustomError

from django.shortcuts import get_object_or_404


class MeetingSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.Meeting
        fields = '__all__'

class MeetingRegister(serializers.Serializer):
    meeting = serializers.IntegerField()
    def create(self, validated_data):
        memeber = self.context.get('user').memeber
        meeting =get_object_or_404( models.Meeting,id=validated_data.get('meeting',-1))
        if models.MeetingAttendies.objects.filter(meeting=meeting,members=memeber).exists():CustomError({'error':'You have registered already'})

        meeting_attendies = models.MeetingAttendies.objects.create(
            meeting=meeting
            ,members=memeber)

        return meeting_attendies



class RegisteredMeetingMembersSerializer(serializers.ModelSerializer):

    memebers = serializers.SerializerMethodField()
    def get_memebers(self,meeting):
        return models.MeetingAttendies.objects.filter(
            meeting=meeting
        ).values('id','members__user__email')

    class Meta:
        model = models.Meeting
        fields = [
            'name','date_for','memebers'
        ]


