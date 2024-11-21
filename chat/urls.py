
from django.urls import path,include
from rest_framework.routers import DefaultRouter

from . import views

route = DefaultRouter()


route.register('',views.ChatRoomViewSet, basename='chatroom')


urlpatterns = [] + route.urls
