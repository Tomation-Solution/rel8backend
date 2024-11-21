from django.shortcuts import render

from utils.custom_exceptions import CustomError
from . import models,serailzer
from rest_framework import mixins,viewsets,status
from utils import custom_response
from rest_framework import permissions
from utils import permissions  as custom_permissions
from rest_framework.decorators import action
from account.models import User
# Create your views here.


"the chat views for every on as long as u authenticated it just a list view"

class ChatRoomViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated,custom_permissions.IsMember]
    queryset = models.ChatRoom.objects.all()
    
    def list(self, request, *args, **kwargs):
        room_name = request.query_params.get('room_name')

        if room_name is None:
            raise CustomError(
                message='Chat Room name is required',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # chat_instances = models.Chat.objects.filter(chat_room__room_name=room_name, user=request.user)
        chat_instances = models.Chat.objects.filter(chat_room__room_name=room_name, user=request.user)
        serializer = serailzer.ChatSerializer(chat_instances, many=True)
        return custom_response.Success_response(msg='Successful',data=serializer.data,status_code=status.HTTP_200_OK) 

    @action(methods=['get'],detail=False)
    def get_users(self,*args,**Kwargs):
        user_list = User.objects.values('id','email')
        return custom_response.Success_response(msg='Success',data=user_list)