from rest_framework import serializers
from . import models


class  LastestUpdatesAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.LastestUpdates
        fields = '__all__'


class  LastestUpdatesMemberSerializer(serializers.ModelSerializer):
    def create(self, validated_data):return None
    def update(self, instance, validated_data):return None


    class Meta: 
        model = models.LastestUpdates
        fields = '__all__'
