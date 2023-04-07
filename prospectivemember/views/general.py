from rest_framework import viewsets
from utils.custom_response import Success_response
from rest_framework import status
from prospectivemember import general_serializer
from ..models import general as general_models
from django.shortcuts import get_object_or_404
from utils.custom_exceptions import CustomError
from utils.permissions import IsProspectiveMember,IsPropectiveMemberHasPaid
from rest_framework.permissions import  IsAuthenticated,AllowAny
from rest_framework.decorators import action
from utils import custom_parsers
from rest_framework.parsers import  FormParser


class CreatePropectiveMemberViewset(viewsets.ViewSet):
    serializer_class = general_serializer.CreatePropectiveMemberSerializer

    def create(self,request,*args,**kwargs):
        serialized= self.serializer_class(data=request.data,context={'request':request})
        serialized.is_valid(raise_exception=True)
        response_info = serialized.save()

        return Success_response('Creation Success',data=[],status_code=status.HTTP_201_CREATED)



class PropectiveMemberHandlesFormOneViewSet(viewsets.ViewSet):
    serializer_class = general_serializer.PropectiveMemberFormOneSerializer
    permission_classes =  [IsAuthenticated,IsProspectiveMember,
                        #    IsPropectiveMemberHasPaid
                           ]
    def create(self,request,*args,**kwargs):
        serialized= self.serializer_class(data=request.data,context={'user':request.user})
        serialized.is_valid(raise_exception=True)
        response_info = serialized.save()
        return Success_response('Submitted, we would get back to you soon',data=[],status_code=status.HTTP_201_CREATED)
    @action(methods=['get'],detail=False)
    def get_data(self, request, *args, **kwargs):
        try:
            form =request.user.prospectivememberprofile.prospectivememberformone

            clean_data =general_serializer.PropectiveMemberFormOneCleaner(instance=form,many=False)
        
            return Success_response('success',data=clean_data.data)
        except: return Success_response('No data found',data=None)
        
    @action(detail=False,methods=['get'])
    def get_admin_rules(self,request,*args,**kwargs):

        admin_rule =  general_models.AdminSetPropectiveMembershipRule.objects.all().first()
        if admin_rule is None:
            raise CustomError({'error':'please reach out to your admin to set text_fields'})
        
        return Success_response('success',data={
            'amount':admin_rule.amount,
            'text_fields':admin_rule.propective_members_text_fields.get('text_fields'),
            'file_fields':admin_rule.propective_members_file_fields.get('file_fields'),
        })
    # def list(self,requeds)


class PropectiveMemberHandlesFormTwoViewSet(viewsets.ViewSet):
    serializer_class = general_serializer.PropectiveMemberFormTwoSerializer
    permission_classes =  [IsAuthenticated,IsProspectiveMember,
                        #    IsPropectiveMemberHasPaid
                           ]
    parser_classes = (custom_parsers.NestedMultipartParser,FormParser,)

    def create(self,request,*args,**kwargs):
        serialized= self.serializer_class(data=request.data,context={'user':request.user})
        return Success_response('Submitted, we would get back to you soon',data=[],status_code=status.HTTP_201_CREATED)

    @action(detail=False,methods=['post'])
    def update_uploadedfiles(self,request,*args,**kwargs):
        pk = request.data.get('id',None)
        form2 = get_object_or_404(general_models.ProspectiveMemberFormTwoFile,id=pk)
        if form2.form_two.prospective_member.user.id != request.user.id:
            raise CustomError({'error':'bad requestt'})
        serialzer= general_serializer.ProspectiveMemberFormTwoFileSerailzer(instance=form2,data=request.data)
        serialzer.is_valid(raise_exception=True)
        data= serialzer.save()

        return Success_response('success',data=data)