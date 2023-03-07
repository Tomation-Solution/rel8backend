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

        if not models.ChatRoom.objects.filter(room_name=room_name).exists():
            raise CustomError(
            message='User does not exist',
            status_code=status.HTTP_400_BAD_REQUEST)
        
        room_name_intance  =models.ChatRoom.objects.get(room_name=room_name)
        data = models.Chat.objects.filter(chat_room=room_name_intance)[:10]
        serialzed = serailzer.ChatSerializer(instance=data,many=True)
        # .order_by('-id').values('message','user__id')[:10]
        data = reversed(serialzed.data)

        return custom_response.Success_response(msg='Successful',data=data,status_code=status.HTTP_200_OK) 

    @action(methods=['get'],detail=False)
    def get_users(self,*args,**Kwargs):
        user_list = User.objects.values('id','email')
        return custom_response.Success_response(msg='Successfully',data=user_list)