from rest_framework import serializers
from . import models




class ManageFaqSerializer(serializers.ModelSerializer):



    class Meta:
        model = models.FAQ
        fields = "__all__"