from  rest_framework import serializers
from .import models




class AdminManageReminderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Reminder
        fields  = ['id','title','body','start_date','start_time','is_active']