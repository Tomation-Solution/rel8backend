from rest_framework import serializers
from . import models
from  utils.notification import NovuProvider
from account.models.user import ExcoRole,CommiteeGroup,User
from account.models.auth import Chapters

class  LastestUpdatesAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.LastestUpdates
        fields = '__all__'


class  LastestUpdatesMemberSerializer(serializers.ModelSerializer):
    def create(self, validated_data):return None
    def update(self, instance, validated_data):return None


    class Meta: 
        model = models.LastestUpdates
        fields = '__all__'




class IndividaulNotification(serializers.Serializer):
    user_ids = serializers.ListField()
    title = serializers.CharField()
    message = serializers.CharField()


    def create(self, validated_data):
        novu = NovuProvider()
        user_ids = validated_data.get('user_ids')
        title= validated_data['title']
        content= validated_data['message']

        novu.send_notification(
        name='on-boarding-notification',
        sub_id=user_ids,
        title=title,
        content=content)
        return dict()


class NotificationByTopicSerializer(serializers.Serializer):
    type = serializers.CharField()#e.g exco 
    title = serializers.CharField()
    content = serializers.CharField()
    id = serializers.IntegerField()

    def create(self, validated_data):
        type = validated_data['type']
        title = validated_data['title']
        content = validated_data['content']
        id = validated_data['id']
        novu = NovuProvider()
        user_ids = []
        if type =='exco':
            exco = ExcoRole.objects.get(id=id)
            for member in exco.member.all():
                user_ids.append(f'{member.user.id}')

        if type =='commitee':
            commitee = CommiteeGroup.objects.get(id=id)
            for member in commitee.members.all():
                user_ids.append(f'{member.user.id}')
        if type == 'chapters':
            users = User.objects.filter(chapter__id=id)
            user_ids = map(lambda user:f'{user.id}',users)

        novu.send_notification(
            name='on-boarding-notification',
            sub_id=user_ids,
            title=title,
            content=content
        )
        return dict()