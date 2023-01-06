import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db import connection

from utils.custom_exceptions import CustomError
from . import models
from django.contrib.auth import get_user_model
from rest_framework import status
from asgiref.sync import sync_to_async
from account.models import user as user_related_models


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.room_name
        self.tenant = self.scope['url_route']['kwargs']['tenant_name']

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        send_user_id = text_data_json['send_user_id']
        # tenant_name
        # print({'schema anme':connection.schema_name})
        print({'schema anme':self.tenant })
        "here we setting the schema using the short name tha was sent from the front end"
        


        await self.validate_user(send_user_id)
        await self.create_chat(send_user_id,message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'send_user_id': send_user_id,
            }
        )

    @sync_to_async
    def validate_user(self,send_user_id):
        connection.set_schema(schema_name=self.tenant)
        "check if user id exist in the data base"
        print({'send_user_id':send_user_id})
        if not get_user_model().objects.filter(id=send_user_id).exists():
            print('does not exist')
            raise CustomError(
            message='User does not exist',
            status_code=status.HTTP_400_BAD_REQUEST
        )
    @sync_to_async
    def create_chat(self,send_user_id,message):
        "we get or create a group name"
        connection.set_schema(schema_name=self.tenant)
        chat_room ,created=  models.ChatRoom.objects.get_or_create(
            room_name=self.room_group_name
        )
        chat_room.save()
        "save the message to that group and u can add it wil the user id"
        user = get_user_model().objects.get(id=send_user_id)
        chat = models.Chat.objects.create(
            chat_room=chat_room,
            message=message,
            user=user
        )
        chat.save()

    async def chatroom_message(self, event):

        message = event['message']
        send_user_id = event['send_user_id']

        await self.send(text_data=json.dumps({
            'message': message,
            'send_user_id': send_user_id,
        }))

    pass




class CommiteeChatRoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.commitee_id = self.scope['url_route']['kwargs']['commitee_id']
        self.room_group_name= self.commitee_id
        self.tenant = self.scope['url_route']['kwargs']['tenant_name']

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,self.channel_name
        )
    
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        send_user_id = text_data_json['send_user_id']

        print({'schema anme':self.tenant })
        "here we setting the schema using the short name tha was sent from the front end"
        
        await self.validate_user(send_user_id)
        await self.create_chat(send_user_id,message)

        await self.channel_layer.group_send(
            self.room_group_name,{
                'type':'chatroom_message',
                'message': message,
                'send_user_id': send_user_id,
            }
        )

    @sync_to_async
    def validate_user(self,send_user_id):
        'this validation first check it the user exist and checks if he is a member and then check if he exists in the commitee'
        connection.set_schema(schema_name=self.tenant)
        if not get_user_model().objects.filter(id=send_user_id).exists():
            print('does not exist')
            raise CustomError(
            message='User does not exist',
            status_code=status.HTTP_400_BAD_REQUEST
        )
        if not user_related_models.CommiteeGroup.objects.filter(id=self.commitee_id).exists():
            raise CustomError(
            message='Commitee does not exist',
            status_code=status.HTTP_400_BAD_REQUEST
        )
        # user = get_user_model().objects.get(id=send_user_id)
        commitee = user_related_models.CommiteeGroup.objects.get(id=self.commitee_id)
        
        if not commitee.members.filter(user=send_user_id).exists():
            raise CustomError(
                message='Access Denied',
                status_code=status.HTTP_400_BAD_REQUEST
            )

    @sync_to_async
    def create_chat(self,send_user_id,message):
        "we get or create a group name"
        connection.set_schema(schema_name=self.tenant)
        chat_room ,created=  models.ChatRoom.objects.get_or_create(
            room_name=self.room_group_name +'commitee'
        )
        chat_room.save()
        user = get_user_model().objects.get(id=send_user_id)
        chat = models.Chat.objects.create(
            chat_room=chat_room,
            message=message,
            user=user
        )
        chat.save()

    async def chatroom_message(self, event):

        message = event['message']
        send_user_id = event['send_user_id']

        await self.send(text_data=json.dumps({
            'message': message,
            'send_user_id': send_user_id,
        }))

    pass
