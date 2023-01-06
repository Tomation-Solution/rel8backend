from django.shortcuts import render
from rest_framework import viewsets,permissions,mixins
from utils import permissions  as custom_permissions
from . import serializer,models
# Create your views here.



class AdminManageReminderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,custom_permissions.IsAdminOrSuperAdmin,
    custom_permissions.Normal_Admin_Must_BelongToACHapter]
    serializer_class = serializer.AdminManageReminderSerializer
    queryset = models.Reminder.objects.all()


class MembersReminderViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = serializer.AdminManageReminderSerializer
    permission_classes = [permissions.IsAuthenticated,custom_permissions.IsMember,]
    queryset = models.Reminder.objects.filter(is_active=True)
    