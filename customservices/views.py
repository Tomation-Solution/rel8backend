from django.shortcuts import render
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from customservices import models,serializers
from utils import permissions as custom_permission
from utils.custom_exceptions import CustomError
from utils.custom_response import Success_response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
class  AdminRel8CustomServicesViewset(ModelViewSet):
    serializer_class =serializers.Rel8CustomServicesSerializer
    queryset  =models.Rel8CustomServices.objects.all()
    permission_classes =[IsAuthenticated,custom_permission.IsAdminOrSuperAdmin]


    @action(methods=['post'],detail=False)
    def handle_request(self,request,*args,**kwargs):
        member_request_id = request.query_params.get('member_request_id')
        status = request.data.get('status')
        member_request = models.Rel8CustomMemberServiceRequests.objects.get(id=member_request_id)
        member_request.status= status
        member_request.save()
        return Success_response('Status Updated Successfully')

    @action(methods=['get'],detail=False)
    def member_submissions(self,request,*args,**kwargs):
        service_id =request.query_params.get('service_id')
        queryset = models.Rel8CustomMemberServiceRequests.objects.filter(custom_service__id=service_id)
        serializer_class = serializers.MembersRel8CustomerServiceSerializer(instance=queryset,many=True)

        return Success_response('Success',data=serializer_class.data)
class MembersRel8CustomerServiceViewset(ViewSet):
    serializer_class = serializers.HandleMemberServiceSubmissions
    permission_classes = [IsAuthenticated,custom_permission.IsMember]


    def create(self,request,*args,**kwargs):
        serializer_class = self.serializer_class(data=request.data,context={'member':request.user.memeber})
        serializer_class.is_valid(raise_exception=True)
        serializer_class.save()

        return Success_response('Submitted')
    def list(self,request,*args,**kwargs):
        service_id =request.query_params.get('service_id')
        queryset = models.Rel8CustomMemberServiceRequests.objects.filter(member=request.user.memeber,custom_service__id=service_id)
        serializer_class = serializers.MembersRel8CustomerServiceSerializer(instance=queryset,many=True)

        return Success_response('Success',data=serializer_class.data)
    
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        instance  =get_object_or_404(
             models.Rel8CustomMemberServiceRequests,
             id = id)
        serializer_class = serializers.MembersRel8CustomerServiceSerializer(instance=instance)
        return Success_response('Success',data=serializer_class.data)

        