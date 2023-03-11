from django.shortcuts import render
from rest_framework import viewsets,permissions
from . import serializer,models
from utils.pagination import CustomPagination
from utils import permissions as custom_permission

class AdminLastestUpdatesViewSet(viewsets.ModelViewSet):
    serializer_class =  serializer.LastestUpdatesAdminSerializer
    queryset = models.LastestUpdates.objects.all()
    permission_classes = [permissions.IsAuthenticated,custom_permission.IsAdminOrSuperAdmin]
    page_size = 15


class MemberLastestUpdatesViewSet(viewsets.ModelViewSet):
    serializer_class =  serializer.LastestUpdatesMemberSerializer
    queryset = models.LastestUpdates.objects.all()
    permission_classes = [permissions.IsAuthenticated,custom_permission.IsMember]
    page_size = 15


