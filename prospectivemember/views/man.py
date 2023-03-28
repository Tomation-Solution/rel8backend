from prospectivemember.models import man_prospective_model as manrelatedPropectiveModels
from prospectivemember import serializer
from rest_framework import viewsets
from utils.custom_response import Success_response
from rest_framework import status
from utils.custom_exceptions import  CustomError 
from rest_framework.permissions import  IsAuthenticated,AllowAny
from rest_framework.decorators import action
from utils.permissions import IsMemberOrProspectiveMember,IsPropectiveMemberHasPaid

class CreateManPropectiveMemberViewset(viewsets.ViewSet):
    serializer_class = serializer.CreateManPropectiveMemberSerializer

    def create(self,request,*args,**kwargs):
        serialized= self.serializer_class(data=request.data,context={'request':request})
        serialized.is_valid(raise_exception=True)
        response_info = serialized.save()

        return Success_response('Creation Success',data=response_info,status_code=status.HTTP_201_CREATED)

class StatusView:
    @action(detail=False,methods=['get'])
    def get_status(self,request,*args,**kwargs):
        return Success_response('..',data=request.user.manprospectivememberprofile.application_status)

class PropectiveMemberManageFormOneViewSet(viewsets.ModelViewSet,StatusView):
    serializer_class = serializer.PropectiveMemberManageFormOneSerializer
    permission_classes=[IsAuthenticated,IsMemberOrProspectiveMember,IsPropectiveMemberHasPaid]
    queryset = manrelatedPropectiveModels.ManProspectiveMemberFormOne.objects.all()



    def create(self, request, *args, **kwargs):
        man_prospective_member_form_one,created= manrelatedPropectiveModels.ManProspectiveMemberFormOne.objects.get_or_create(prospective_member=request.user.manprospectivememberprofile)

        serializer_class = self.serializer_class(data=request.data,instance=man_prospective_member_form_one)
        serializer_class.is_valid(raise_exception=True)
        instance = serializer_class.save()

        clean_data =self.serializer_class(instance=instance,many=False)
        return Success_response('Update Successfull',data=clean_data.data,status_code=status.HTTP_200_OK)

    def get_queryset(self):
        query_set = self.queryset.filter(prospective_member=self.request.user.manprospectivememberprofile)
        return query_set


class PropectiveMemberManageFormTwo(viewsets.ModelViewSet,StatusView):
    serializer_class = serializer.PropectiveMemberManageFormTwoSerializer
    queryset = manrelatedPropectiveModels.ManProspectiveMemberFormTwo.objects.all()
    permission_classes=[IsAuthenticated,IsMemberOrProspectiveMember,IsPropectiveMemberHasPaid]

    def create(self, request, *args, **kwargs):
        man_prospective_member_form_one,created= manrelatedPropectiveModels.ManProspectiveMemberFormTwo.objects.get_or_create(prospective_member=request.user.manprospectivememberprofile)

        serializer_class = self.serializer_class(data=request.data,instance=man_prospective_member_form_one)
        serializer_class.is_valid(raise_exception=True)
        instance = serializer_class.save()

        clean_data =self.serializer_class(instance=instance,many=False)
        return Success_response('Update Successfull',data=clean_data.data,status_code=status.HTTP_200_OK)

    def get_queryset(self):
        query_set = self.queryset.filter(prospective_member=self.request.user.manprospectivememberprofile)
        return query_set

