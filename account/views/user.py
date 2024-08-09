from django import views
from rest_framework import viewsets,generics

from rest_framework import permissions
from rest_framework.decorators import action,api_view,permission_classes
from Dueapp.models import Due_User,DeactivatingDue_User
from Rel8Tenant.task import finicial_report
from utils.custom_exceptions import CustomError
from ..serializers import user
from utils import custom_response
from rest_framework import status
from utils import permissions  as custom_permissions
from ..serializers import user as user_serializer 
from ..models import user as  user_models
from account.models import auth as  auth_models
from rest_framework.decorators import action
from rest_framework.views import APIView
from event import models
from rest_framework.parsers import FormParser
from django.db.models import F
from utils.custom_parsers import NestedMultipartParser
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from ..serializers import auth as auth_serializer
from rest_framework.response import Response
from django.db import transaction

# from


class GetExistingChapters(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        chapters_instances = auth_models.Chapters.objects.all()
        serializer_class  = auth_serializer.ManageChapters(chapters_instances, many=True)
        return custom_response.Success_response(msg="Success",data=serializer_class.data)


class RegisterUserToChapter(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated,custom_permissions.IsAdminOrSuperAdmin]
    serializer_class  = user.RegisterUserToChapterView

    def list(self,request,format=None):
        chapters =auth_models.Chapters.objects.all().values()
        return custom_response.Success_response(msg="Success",data=chapters)

    def create(self,request,format=None):

        serialize = self.serializer_class(data=request.data)
        serialize.is_valid(raise_exception=True)
        serialize.save()
        return custom_response.Success_response(msg="Created Successful",data=[])

class CreateAlumni(generics.CreateAPIView):
    serializer_class = user.CreateAlumniSerializers    
    permission_classes = [permissions.IsAuthenticated]
    # queryset = rel8TenantModels.Client.objects.all()

    def post(self, request, *args, **kwargs):
        serializer =self.get_serializer(data=request.data,)
        serializer.is_valid(raise_exception=True)
        if(serializer.is_valid()):
            serializer.save()
            return custom_response.Success_response(msg='alumni created successfully',data=serializer.data,status_code=status.HTTP_201_CREATED)
        print(serializer.errors)
        raise CustomError({"error":"Some Error Occured"},)
        # return super().post(request, *args, **kwargs)

class CreateAnyAdminType(viewsets.ViewSet):
    # permission_classes = [permissions.IsAuthenticated,custom_permissions.IsAdminOrSuperAdmin
    # ]#chnage to admin late
    serializer_class=user.CreateAnyAdminTypeSerializer
    @action(detail=False,methods=['post'])
    def create_superadmin(self,request,pk=None):
        'you have to b a super admin to create a super admin'
        # if request.user.user_type not in ['super_admin']:
        #     raise CustomError({"error":"You need to be a super admin to create another super admin"})
        serialize = self.serializer_class(data=request.data,context={"adminType":"super_admin"})
        serialize.is_valid(raise_exception=True)
        user =serialize.save()
        return custom_response.Success_response(msg='Super Admin created successfully',data=[{
             "user_id":user.id,
             "email":user.email,
            "user_type":user.user_type
        }],status_code=status.HTTP_201_CREATED)


    @action(detail=False,methods=['post'])
    def create_admin(self,request,pk=None):
        'you have to b a super admin to create a  admin'
        serialize = self.serializer_class(data=request.data,context={"adminType":"admin"})
        serialize.is_valid(raise_exception=True)
        user = serialize.save()
        return custom_response.Success_response(msg='Admin created successfully',data=[{
            "user_id":user.id,
             "email":user.email,
            "user_type":user.user_type
        }],status_code=status.HTTP_201_CREATED)

class ManageAssigningExcos(viewsets.ViewSet):
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes =  [permissions.IsAuthenticated]
        else:
            self.permission_classes=[permissions.IsAuthenticated,custom_permissions.IsAdminOrSuperAdmin]
        return super(ManageAssigningExcos,self).get_permissions()

    def create(self,request,format=None):
        'here admin can create more exco postion type'
        serialized = user_serializer.CreateExcoRole(data=request.data,context={'request':request})

        serialized.is_valid(raise_exception=True)
        data =serialized.save()
        # clead_data = user_serializer.CreateExcoRole(data,many=False)
        return custom_response.Success_response(msg='Exco Role created successfully',data=[],status_code=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        if not user_models.ExcoRole.objects.filter(id=pk).exists():
            raise CustomError({"error":"ExcoRole Does not exist"})
        chapter_id = request.data.get('chapter_id', None)
        new_chapter_instance = None
        if chapter_id is not None:
            try:
                new_chapter_instance = auth_models.Chapters.objects.get(id=chapter_id)
            except auth_models.Chapters.DoesNotExist:
                raise CustomError(message="Chapter is not found!", status_code=404)

        exco_role = user_models.ExcoRole.objects.get(id=pk)
        serialized = user_serializer.CreateExcoRole(instance=exco_role,data=request.data,context={"request":request, "chapter": new_chapter_instance})
        serialized.is_valid(raise_exception=True)
        updated_instance =serialized.save()
        clean_data = user_serializer.CreateExcoRole(updated_instance,many=False)
        return custom_response.Success_response(msg='Exco Role Updated successfully',data=clean_data.data,status_code=status.HTTP_201_CREATED)

    def list(self,request,format=None):
        data = user_models.ExcoRole.objects.all()
        clean_data = user_serializer.CreateExcoRole(data,many=True)
        return custom_response.Success_response(msg='Success',data=clean_data.data,status_code=status.HTTP_200_OK)
    
    def destroy(self,request, pk=None):
        try:
            instance = user_models.ExcoRole.objects.get(id=pk)
        except user_models.ExcoRole.DoesNotExist:
            raise CustomError({'exco_role':'This Role does not exist or must have been deleted'})
        
        exco_members = instance.member.all()
        instance.delete()
        for member in exco_members:
            member.is_exco = False
            member.save()
        return custom_response.Success_response(msg='Deleted exco role.',data=[],status_code =status.HTTP_204_NO_CONTENT)


class ListExcoRolesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        exco_role_id = request.query_params.get('exco_role_id', None)

        if exco_role_id is not None:
            exco_role = get_object_or_404(user_models.ExcoRole, id=exco_role_id)
            serializer = user_serializer.ExcoRoleSerializer(exco_role, many=False)
            return custom_response.Success_response(msg='Success', data=serializer.data, status_code=status.HTTP_200_OK)

        exco_roles = user_models.ExcoRole.objects.all()
        serializer = user_serializer.ExcoRoleSerializer(exco_roles, many=True)
        return custom_response.Success_response(msg='Success', data=serializer.data, status_code=status.HTTP_200_OK)



class RemoveMemberFromExcoRoleView(APIView):
    permission_classes = [custom_permissions.IsAdminOrSuperAdmin]

    def post(self, request, *args, **kwargs):
        member_name = request.data.get('member_name', None)
        
        if member_name is None:
            return Response({'error': 'Member name is required.'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            try:
                # Find the member with the given name
                member = user_models.Memeber.objects.get(name=member_name)
            except user_models.Memeber.DoesNotExist:
                return Response({'error': 'Member not found.'}, status=status.HTTP_404_NOT_FOUND)

            # Find ExcoRoles where the member is associated
            exco_roles = user_models.ExcoRole.objects.filter(member=member)
            
            if not exco_roles.exists():
                return Response({'message': 'No ExcoRoles found for the given member.'}, status=status.HTTP_404_NOT_FOUND)

            # Remove the member from all associated ExcoRoles
            for exco_role in exco_roles:
                exco_role.member.remove(member)

            return Response({'message': 'Member successfully removed from ExcoRoles.'}, status=status.HTTP_200_OK)


class AdminRelatedViews(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated,custom_permissions.IsAdminOrSuperAdmin]#chnage to admin late
    @action(detail=False,methods=['get'])
    def dashboard_info(self,request,pk=None):
        num_of_members = user_models.Memeber.objects.all().count()
        event_count = models.Event.objects.all().count()
        exco_member = user_models.Memeber.objects.filter(is_exco=True).count()
        # _member = user_models.Memeber.objects.filter(is_exco=True).count()
        amount_owing = 0
        total_income = 0
        for members  in user_models.Memeber.objects.all():
            "get all members and get the amount they are owing"
            amount_owing=+members.amount_owing
        
        for user in Due_User.objects.all().filter(is_paid=True):
            "get only the paid instance and get their amount"
            total_income =+user.amount

        for user in DeactivatingDue_User.objects.all().filter(is_paid=True):
            "get only the paid instance and get their amount"
            total_income =+user.amount
        
        return custom_response.Success_response(msg='successful',data=[{
                "num_of_members":num_of_members,
                "event_count":event_count,
                "exco_member":exco_member,
                "total_income":total_income,
                "amount_owing":amount_owing,
        }],status_code=status.HTTP_200_OK)
   

class MemberListInfo(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = user.MemberSerializer





    @action(detail=False,methods=['get'])
    def get_all_members(self,request,pk=None):

        members  = user_models.Memeber.objects.all()
        serialized = self.serializer_class(members,many=True)
        return  custom_response.Success_response(msg='successful',data=serialized.data,status_code=status.HTTP_200_OK)

    @action(detail=False,methods=['get'])
    def get_all_exco(self,request,pk=None):
        exco_members = user_models.Memeber.objects.all().filter(is_exco=True)
        # exco_members = user_models.ExcoRole.objects.all()

        serialized = self.serializer_class(exco_members,many=True)
        return custom_response.Success_response(msg='successful',data=serialized.data,status_code=status.HTTP_200_OK)
    @action(detail=False,methods=['post'])
    def delete_member_bio(self,request,pk=None):
        serializer = user.HandleDeleteMemberBioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return custom_response.Success_response(msg='deleted successfully',status_code=status.HTTP_204_NO_CONTENT)


    @action(detail=False,methods=['get'],permission_classes = [permissions.IsAuthenticated,custom_permissions.IsMember])
    def my_profile(self,request,pk=None):
        "this would get the current logged in memebr profile"
        another_user_id = self.request.query_params.get("another_user_id",None)
        user =None
        if another_user_id is None:
            "if it none this means u want to get the current user profile"
            user=request.user
        else:
            user = another_user_id

        # finicial_report()
        filterterd_user_instance = user_models.Memeber.objects.all().filter(user=user)
        serialized = self.serializer_class(filterterd_user_instance,many=True)
        return custom_response.Success_response(msg='successful',data=serialized.data,status_code=status.HTTP_200_OK)
   
    @action(detail=False,methods=['post'],permission_classes =[permissions.IsAuthenticated,custom_permissions.IsMember],
    parser_classes=(NestedMultipartParser,FormParser,))
    def update_profile_img(self,request,format=False):
        print('hellp')
        print(request.data)
        logged_in_user = user_models.User.objects.get(id=request.user.id)
        data = user.UserProfilePicsSerializer(logged_in_user,data=request.data)
        data.is_valid(raise_exception=True)
        url = data.save()
        if logged_in_user.photo:url = logged_in_user.photo.url
        else:url = ''
        return  custom_response.Success_response(msg="Success",data=[url],status_code=status.HTTP_200_OK)
    @action(detail=False,methods=['post'],permission_classes =[permissions.IsAuthenticated,custom_permissions.IsMember])
    def update_profile(self,request,format=False):
        logged_in_user = user_models.User.objects.get(id=request.user.id)
        member = user_models.Memeber.objects.get(user=logged_in_user)
        # instance =user_models.UserMemberInfo.objects.filter(member=member)
        serialized = user.MemberProfileUpdateSerializer(data=request.data,many=True,context={'user':request.user})
        serialized.is_valid(raise_exception=True)
        serialized.save()
        return custom_response.Success_response(msg='Updated',data=[],status_code=status.HTTP_200_OK)
    

class MemberBioViewSet(viewsets.ModelViewSet):
    serializer_class =user.MemberUpdateBioSerializer
    queryset = user_models.Memeber.objects.all()
    permission_classes = [permissions.IsAuthenticated,custom_permissions.IsMember]

    # def create(self, request, *args, **kwargs):
    #     serialized = self.serializer_class(data=request.data,context={'user':request.user})
    #     serialized.is_valid(raise_exception=True)
    #     d  = serialized.save()
    #     return custom_response.Success_response(msg='Successfull',data=[])

    def update(self, request, *args, **kwargs):
        instance = user_models.Memeber.objects.get(id=request.user.memeber.id)
        instance.bio=request.data.get('bio',instance.bio)
        instance.save()
        serialized = self.serializer_class(instance=instance,data=request.data,context={'user':request.user})
        serialized.is_valid(raise_exception=True)
        data =serialized.save()

        clean_data = user.MemberSerializer(instance=instance,context={'user':request.user})
        return custom_response.Success_response('Updated',data=clean_data.data)
    

@api_view(['GET',])
@permission_classes([permissions.IsAuthenticated,custom_permissions.IsMember])
def profile(request,format=False):
    data = dict()

    memeber =  user_models.Memeber.objects.get(user=request.user)
    member_info = user_models.UserMemberInfo.objects.filter(member=memeber).values('value','name','id')

    data['amount_owing']=memeber.amount_owing
    data['is_exco']=memeber.is_exco
    data['member_id'] = memeber.id
    data['is_financial']=memeber.is_financial
    data['more_info'] =member_info
    return custom_response.Success_response(msg="Success",data=[data],status_code=status.HTTP_200_OK)

@api_view(['POST',])
@permission_classes([permissions.IsAuthenticated,])
def council_members(request,*args,**kwargs):
    council  = get_object_or_404(user_models.ExcoRole,id=kwargs['pk'])
    council_members = council.member.all()
    serialized = user.MemberSerializer(council_members,many=True)
    return custom_response.Success_response(msg='successful',data=serialized.data,status_code=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated,])
def get_membershipgrade(request,*args,**kwargs):
    grades = user_models.MemberShipGrade.objects.all().values('id','name')
    return custom_response.Success_response(msg='successful',)
                                            


class UpdateMemberInfoViewSet(viewsets.ModelViewSet):
    permission_classes =[ permissions.IsAuthenticated,
                        #  custom_permissions.IsAdminOrSuperAdmin
                         ]
    queryset = user_models.UserMemberInfo.objects.all()
    serializer_class =user.AdminUpdateMemberInfoCleaner


    def create(self, request, *args, **kwargs):
        return

    def update(self, request, *args, **kwargs):
        user = request.user
        loggedinMember = user_models.Memeber.objects.get(user=user.id)
        user_member_info = user_models.UserMemberInfo.objects.filter(member=loggedinMember.id)

        serailzer = self.serializer_class(instance=user_member_info,data=request.data)
        serailzer.is_valid(raise_exception=True)
        d=serailzer.save()
        return custom_response.Success_response('Success',data=None )
    





class ForgotPasswordViewSet(viewsets.ViewSet):
    permission_classes=[AllowAny]

    @action(methods=['post'],detail=False,permission_classes=[AllowAny])
    def request_password_change(self,request,*args,**kwargs):
        print({'d':request.data})
        serialzier= user_serializer.PasswordResetRequestSerializer(data=request.data,context={'request':request})
        serialzier.is_valid(raise_exception=True)
        serialzier.save()
        return custom_response.Success_response('Forgot password link sent to your mail!')
    
    @action(methods=['post'],detail=False,permission_classes=[AllowAny])
    def rest_password(self,request,*args,**kwargs):
        serialzier =user_serializer.PasswordResetConfirmationSerializer(data=request.data,context={'request':request})
        serialzier.is_valid(raise_exception=True)
        serialzier.save()
        return custom_response.Success_response('Password Rest Successfully')