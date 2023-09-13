from rest_framework import serializers
from customservices import models
from django.shortcuts import get_object_or_404
from account.models.user import Memeber

class  Rel8CustomServicesSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.Rel8CustomServices
        fields ='__all__'


    # def create(self, validated_data):
        

class HandleMemberServiceSubmissions(serializers.Serializer):
    custom_service = serializers.IntegerField()
    fields_subbission = serializers.JSONField()
    files = serializers.ListField(
        child =serializers.FileField(
            max_length=10000000,
            use_url=False,
            write_only=True
        ),required=False)
    

    def create(self, validated_data):
        files = validated_data.get('files',[])
        fields_subbission = validated_data.get('fields_subbission')
        custom_service = validated_data.get('custom_service',-1)
        rel8_custom_services = get_object_or_404(models.Rel8CustomServices,id= custom_service,)
        member = self.context.get('member')
        rel8_custom_member_servicerequests,created=models.Rel8CustomMemberServiceRequests.objects.get_or_create(
            custom_service=rel8_custom_services,
            member = member,
            status='pending'
        )
        for field in fields_subbission:
            filed_instance,created = models.Rel8CustomMemberServiceRequestsText.objects.get_or_create(
                customMember_service_request=rel8_custom_member_servicerequests,
                name= field.get('name')
            ) 
            filed_instance.value = field.get('value')
            filed_instance.save()

        # rel8_custom_services
        # models.Rel8CustomMemberServiceRequests
        for file in files:
            name = file.name.split('.')[0]
            fileInstance,created = models.Rel8CustomMemberServiceRequestTextFile.objects.get_or_create(
                name= name,
                customMember_service_request=rel8_custom_member_servicerequests
            )
            fileInstance.value=file
            fileInstance.save()
        return dict()
    

class MembersRel8CustomerServiceSerializer(serializers.ModelSerializer):
    fields_subbission = serializers.SerializerMethodField()
    files =serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    service_name = serializers.SerializerMethodField()
    def get_full_name(self,instance:models.Rel8CustomMemberServiceRequests):
        return instance.member.full_name
    def get_files(self,instance:models.Rel8CustomMemberServiceRequests):
        data = []
        for i in  models.Rel8CustomMemberServiceRequestTextFile.objects.filter( customMember_service_request=instance):
            current = {'id':i.id,'name':i.name}
            try:
                current['value']= i.value.url
            except:
                current['value'] = ''
            data.append(current)
        return data
    # .values(
    #         'id','value','name'
    #     )
    def get_service_name(self,instance:models.Rel8CustomMemberServiceRequests):
        return instance.custom_service.service_name
    def get_fields_subbission(self,instance:models.Rel8CustomMemberServiceRequests):

        return models.Rel8CustomMemberServiceRequestsText.objects.filter(
            customMember_service_request=instance).values('id','value','name')


    class Meta:
        model = models.Rel8CustomMemberServiceRequests
        fields =['id','status','custom_service','amount','fields_subbission','files',
                 'full_name','service_name'
                 ]


    