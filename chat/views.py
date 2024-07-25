from django.shortcuts import render

from utils.custom_exceptions import CustomError
from . import models,serailzer
from rest_framework import mixins,viewsets,status
from utils import custom_response
from rest_framework.decorators import action
from account.models import User
# Create your views here.


"the chat views for every on as long as u authenticated it just a list view"

class ChatRoomViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = models.ChatRoom.objects.all()


    def list(self, request, *args, **kwargs):
        room_name = request.query_params.get('room_name')
        try:
            room_name_instance = models.ChatRoom.objects.get(room_name=room_name)
        except ChatRoom.DoesNotExist:
            raise CustomError(
            message='Chat room does not exist',
            status_code=status.HTTP_404_NOT_FOUND)
        
        chat_instances = models.Chat.objects.filter(chat_room=room_name_instance)[:10]
        serialzed = serailzer.ChatSerializer(instance=chat_instances,many=True)
        serailzer.is_valid(raise_exception=True)
        # .order_by('-id').values('message','user__id')[:10]
        chats = reversed(serialzed.data)

        return custom_response.Success_response(msg='Successful',data=chats,status_code=status.HTTP_200_OK) 

    @action(methods=['get'],detail=False)
    def get_users(self,*args,**Kwargs):
        user_list = User.objects.values('id','email')
        return custom_response.Success_response(msg='Successfully',data=user_list)