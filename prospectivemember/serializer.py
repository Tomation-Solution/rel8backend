from rest_framework import serializers
from .models import man_prospective_model
from django.contrib.auth import get_user_model as USER
from utils.custom_exceptions import  CustomError 
from mymailing import tasks as mymailing_task


class CreateManPropectiveMemberSerializer(serializers.ModelSerializer):


    def create(self, validated_data):
        email = validated_data.get('email',None)
        cac = validated_data.get('cac_registration_number')
        if USER().objects.filter(email=email).exists():
            raise CustomError({'error':'user email already exists'})
        user = USER().objects.create_user(
            email=email,
            password=cac,
            user_type='prospective_members'
        )
        user.is_prospective_Member=True
        user.save()

        man_propective = man_prospective_model.ManProspectiveMemberProfile.objects.create(
            user=user
            **validated_data
        )
        mymailing_task.send_activation_mail.delay(user.id,user.email)

        return man_propective
    class Meta:
        model  =man_prospective_model.ManProspectiveMemberProfile
        fields = '__all__'
        read_only_fields = ['user','paystack','has_paid']


class PropectiveMemberManageFormOneSerializer(serializers.ModelSerializer):

    def create(self, validated_data):return None

    class Meta:
        model = man_prospective_model.ManProspectiveMemberFormOne
        fields = '__all__'
        read_only_fields =['prospective_member']

    
class PropectiveMemberManageFormTwoSerializer(serializers.ModelSerializer):

    def create(self, validated_data):return None
    class Meta:
        model = man_prospective_model.ManProspectiveMemberFormTwo
        fields = '__all__'
        read_only_fields =['prospective_member']

    

