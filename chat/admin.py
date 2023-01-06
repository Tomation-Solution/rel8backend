from typing import Sequence
from django.contrib import admin
from . import models
# Register your models here.




class Messages(admin.TabularInline):
    model =  models.Chat
    extra: int=0
class ChatRoom(admin.ModelAdmin):
    inlines =[Messages]


admin.site.register(models.ChatRoom,ChatRoom)