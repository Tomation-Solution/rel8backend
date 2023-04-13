from rest_framework import viewsets
from utils.custom_response import Success_response
from rest_framework import status
from prospectivemember import general_serializer
from ..models import general as general_models
from django.shortcuts import get_object_or_404
from utils.custom_exceptions import CustomError
from utils.permissions import  IsAdminOrSuperAdmin, IsProspectiveMember,IsPropectiveMembersHasPaid_general
from rest_framework.permissions import  IsAuthenticated,AllowAny
from rest_framework.decorators import action
from utils import custom_parsers
from rest_framework.parsers import  FormParser
from rest_framework.decorators import parser_classes as decoratorBasedParserClasses
from rest_framework.decorators import permission_classes

class CreatePropectiveMemberViewset(viewsets.ViewSet):
    serializer_class = general_serializer.CreatePropectiveMemberSerializer

    def create(self,request,*args,**kwargs):
        serialized= self.serializer_class(data=request.data,context={'request':request})
        serialized.is_valid(raise_exception=True)
        response_info = serialized.save()

        return Success_response('Creation Success',data=[],status_code=status.HTTP_201_CREATED)

class ProfileStatus:

    @action(detail=False,methods=['get'])
    def get_status(self,request,*args,**kwargs):

        profile = request.user.prospectivememberprofile
        return Success_response('success',data={
            'status':profile.application_status
        })

class PropectiveMemberHandlesFormOneViewSet(viewsets.ViewSet,ProfileStatus):
    serializer_class = general_serializer.PropectiveMemberFormOneSerializer
    permission_classes =  [IsAuthenticated,IsProspectiveMember,
                           IsPropectiveMembersHasPaid_general
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

    @action(detail=False,methods=['get'],permission_classes=[IsAuthenticated,IsProspectiveMember])
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


class PropectiveMemberHandlesFormTwoViewSet(viewsets.ViewSet,ProfileStatus):
    serializer_class = general_serializer.PropectiveMemberFormTwoSerializer
    permission_classes =  [IsAuthenticated,IsProspectiveMember,
                        IsPropectiveMembersHasPaid_general
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
    
    @action(detail=False, methods=['post'])
    def delete_file(self,request,*args,**kwargs):
        pk = request.data.get('id',None)
        form2 = get_object_or_404(general_models.ProspectiveMemberFormTwoFile,id=pk)
        form2.delete()
        return Success_response('deleted success',data=[])
    
    def list(self,request,*args,**kwargs):
        # PropectiveMemberFormTwoCleaner
        form_two,_=general_models.ProspectiveMemberFormTwo.objects.get_or_create(prospective_member=request.user.prospectivememberprofile)
        serilzer = general_serializer.PropectiveMemberFormTwoCleaner(instance=form_two,many=False)

        return Success_response('Success',data=serilzer.data)

class UpdateFomrTwoViewSet(viewsets.ViewSet,ProfileStatus):
    permission_classes =  [IsAuthenticated,IsProspectiveMember,
                          IsPropectiveMembersHasPaid_general
                           ]
    # parser_classes = (custom_parsers.NestedMultipartParser,FormParser,)
    serializer_class = general_serializer.PropectiveMemberFormTwoSerializerUpdate

    def create(self,request,*args,**kwargs):
        # print({'data':request.data})
        serializer_class =general_serializer.PropectiveMemberFormTwoSerializerUpdate(data=request.data,context={'user':request.user})

        return Success_response('updated successfully',data=[])


class AdminManageProspectiveRuleViewSet(viewsets.ViewSet):
    serializer_class =general_serializer.AdminManageProspectiveRuleSerializer
    permission_classes = [IsAuthenticated,IsAdminOrSuperAdmin]
    queryset = general_models.AdminSetPropectiveMembershipRule.objects.all()

    

    def list(self, request, *args, **kwargs):
        rule,_ = general_models.AdminSetPropectiveMembershipRule.objects.get_or_create(
            id=133,
        )
        serialzer =self.serializer_class(many=False,instance=rule,)

        return Success_response(msg='Success',data=serialzer.data)

    def create(self, request, *args, **kwargs):
        rule,_ = general_models.AdminSetPropectiveMembershipRule.objects.get_or_create(
            id=133,
        )
        serialzer =self.serializer_class(data=request.data,instance=rule,partial=True)
        serialzer.is_valid(raise_exception=True)
        d =serialzer.save()
        return  Success_response(msg='Updated',)
    

    @action(detail=False,methods=['get'])
    def get_submissions(self,request,*args,**kwargs):

        all_propective_member_profiles = general_models.ProspectiveMemberProfile.objects.all()
        clean_data = general_serializer.ProspectiveMemberCleaner(instance=all_propective_member_profiles,many=True)
        

        return Success_response('success',data=clean_data.data,)
    
    @action(detail=False,methods=['post'])
    def update_prospective_member_status(self,request,*args,**kwargs):
        pk = request.data.get('id',-1)
        status = request.data.get('status','kk')
        if not status in ['approval_in_progress','approval_in_principle_granted','final_approval']:
            raise CustomError({'error':'choices are aproval in progress , approval in price grated  and final approval'})
        profile = get_object_or_404(general_models.ProspectiveMemberProfile,id=pk)
        profile.application_status = status
        profile.save()

        return Success_response('Updated status',data=[])
    

        