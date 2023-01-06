from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<tenant_name>\w+)/(?P<room_name>\w+)/$', consumers.ChatRoomConsumer.as_asgi()),
    re_path(r'ws/commitee_chat/(?P<tenant_name>\w+)/(?P<commitee_id>\w+)/$',consumers.CommiteeChatRoomConsumer.as_asgi())
]

