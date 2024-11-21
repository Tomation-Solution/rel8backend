
from . import models
from rest_framework import serializers


class ChatSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField()
    user__id = serializers.SerializerMethodField()

    def get_user__id(self, obj):
        return obj.user.id if obj.user else None

    def get_full_name(self,instance):
        user = instance.user
        user_full_name = None
        if user:
            if user.user_type == 'members':
                user_full_name = user.memeber.full_name
            else:
                user_full_name = 'admin'
        
        return user_full_name
        

    class Meta:
        model = models.Chat
        fields = ['message','user__id','full_name','id']
        order_by  =(
            ('-id',)
        )