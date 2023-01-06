from rest_framework import serializers
from . import models



class MinuteSerializers(serializers.ModelSerializer):



    class Meta:
        model = models.Minute
        fields =  "__all__"