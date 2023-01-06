from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.



class ChatRoom(models.Model):
    '''
    the room name would be formated by 
    "id-id" the greater number will be in the front so we can use split to check the two id

    but if is_group is sent to the socket then we just use the group like that
    '''
    room_name= models.TextField()
    def __str__(self) -> str: return f'{self.room_name}'



class Chat(models.Model):
    chat_room =models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    message = models.TextField()
    # this is the sendeer
    user = models.ForeignKey(get_user_model(),null=True,on_delete=models.SET_NULL)

    
