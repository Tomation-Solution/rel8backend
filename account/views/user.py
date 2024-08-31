from django import views
from rest_framework import viewsets,generics
import threading
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
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
from mymailing.EmailConfirmation import activateEmail
from django.db import connection


# from


class GetExistingChapters(APIView):
    permission_classes = [permissions.AllowAny]

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

        #Send Activation Email
        thread= threading.Thread(target=activateEmail,args=[user,user.email,connection.schema_name])
        thread.start()

        return custom_response.Success_response(msg='Admin created successfully. Check your mail for verification!',data=[{
            "user_id":user.id,
             "email":user.email,
            "user_type":user.user_type
        }],status_code=status.HTTP_201_CREATED)

class ManageAssigningExcos(viewsets.ViewSet):
    """
    A ViewSet for CRUD operations on ExcoRole model.
    """

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes =  [permissions.IsAuthenticated]
        else:
            self.permission_classes=[permissions.IsAuthenticated,custom_permissions.IsAdminOrSuperAdmin]
        return super(ManageAssigningExcos,self).get_permissions()

    def list(self, request):
        """
        Retrieve all ExcoRole instances.
        """
        queryset = user_models.ExcoRole.objects.all()
        serializer = user_serializer.CreateExcoRoleSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Create a new ExcoRole instance.
        """
        chapter = get_object_or_404(auth_models.Chapters, id=request.data.get('chapter_id'))
        serializer = user_serializer.CreateExcoRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        exco_role = serializer.save(chapter=chapter)

        # Handle member associations
        member_ids = request.data.get('member_ids', [])
        for member_id in member_ids:
            member = get_object_or_404(user_models.Memeber, id=member_id)
            exco_role.member.add(member)

        return Response({'message': 'Success'}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """
        Update an existing ExcoRole instance.
        """
        exco_role = get_object_or_404(user_models.ExcoRole, pk=pk)
        serializer = user_serializer.CreateExcoRoleSerializer(exco_role, data=request.data)
        serializer.is_valid(raise_exception=True)
        exco_role = serializer.save()

        # Handle member associations
        member_ids = request.data.get('member_ids', [])
        exco_role.member.clear()
        for member_id in member_ids:
            member = get_object_or_404(user_models.Memeber, id=member_id)
            exco_role.member.add(member)

        return Response({'message': 'Success'}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """
        Delete an existing ExcoRole instance.
        """
        exco_role = get_object_or_404(user_models.ExcoRole, pk=pk)
        exco_role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



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



class MemberShipGradeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    # LIST all MemberShipGrade
    def list(self, request):
        grades = user_models.MemberShipGrade.objects.all()
        serializer = user.MemberShipGradeSerializer(grades, many=True)
        return Response(serializer.data)

    # RETRIEVE a specific MemberShipGrade by ID
    def retrieve(self, request, pk=None):
        grade = get_object_or_404(user_models.MemberShipGrade, pk=pk)
        serializer = user.MemberShipGradeSerializer(grade)
        return Response(serializer.data)

    # UPDATE a specific MemberShipGrade by ID
    def update(self, request, pk=None):
        grade = get_object_or_404(user_models.MemberShipGrade, pk=pk)
        serializer = user.MemberShipGradeSerializer(grade, data=request.data)
        if serializer.is_valid():
            membership_grade = serializer.save()
            # Get the list of member IDs from the request data
            member_ids = request.data.get('member_ids')

            if member_ids:
                # Fetch all valid members whose IDs are in the list
                members = user_models.Memeber.objects.filter(id__in=member_ids)

                if members.exists():
                    # Add all members to the MemberShipGrade
                    membership_grade.member.set(members)
                    membership_grade.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE a specific MemberShipGrade by ID
    def destroy(self, request, pk=None):
        grade = get_object_or_404(user_models.MemberShipGrade, pk=pk)
        grade.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        serializer = user.MemberShipGradeSerializer(data=request.data)
        
        # Validate the MemberShipGrade data
        if serializer.is_valid():
            # Save the new grade
            membership_grade = serializer.save()

            # Get the list of member IDs from the request data
            member_ids = request.data.get('member_ids')

            if member_ids:
                # Fetch all valid members whose IDs are in the list
                members = user_models.Memeber.objects.filter(id__in=member_ids)

                if members.exists():
                    # Add all members to the MemberShipGrade
                    membership_grade.member.add(*members)
                    membership_grade.save()

            # Return the created grade with a success response
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Return validation errors if the data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
