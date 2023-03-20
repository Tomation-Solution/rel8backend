import json
from account.task import regiter_user_to_chat,charge_new_member_dues
from mymailing import tasks as mymailing_task
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from utils.custom_exceptions import CustomError
from utils.custom_response import Success_response
from rest_framework import status
from ..serializers import auth as auth_serializers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from utils import permissions as custom_permission
from ..models import auth as auth_models
from ..models import user as user_models
from utils import custom_parsers
from rest_framework.decorators import action,permission_classes
from rest_framework.generics import GenericAPIView
from mailing.models import EmailInvitation
from datetime import datetime
from django.db.models import Q
# create Super user of the Alumni which is the owner





class EmailValidateView(GenericAPIView):
    """
    Account activation with email view
    """
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = auth_serializers.EmailValidateSerializer

    def post(self,request):
        
        key = request.data.get("key", None)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
                
            if   EmailInvitation.objects.filter(key=key).exists():
                email_activation_query = EmailInvitation.objects.filter(
                    key=key
                )
                print("helo ")
                confirm_query = email_activation_query.confirmable()
                if confirm_query.count() == 1:
                    email_activation_object: EmailInvitation = (
                        confirm_query.first()
                    )
                    email_activation_object.activate()

                    return Success_response(msg="Validated Successfully ",data=[],status_code=status.HTTP_200_OK)
                else:
                    activated_query = email_activation_query.filter(activated=True)
                    if activated_query.exists():
                        return Success_response(msg= "Your email has already been confirmed",data=[],status_code=status.HTTP_200_OK)
                
            raise CustomError({"error":"Bad Key"})

            
class RegisterSuperAdmin(CreateAPIView):
    serializer_class  =auth_serializers.RegisterAdminUser
    permission_classes =[AllowAny]

    def post(self,request):
        serializedData = self.serializer_class(data=request.data)

        if serializedData.is_valid(raise_exception=True):
            user = serializedData.save()
            print(user)
            return Success_response(msg="Admin Successfully Created",data=[],status_code=status.HTTP_200_OK)
        
        raise CustomError({"error":"some error occured"})

# end poing to create alumni which should include excel file that contain the list of users

# verify u a user with exisiting excel if it true then create that user
    # we would use a format in the excel that will allow us to use as the verifiction field

class Login(ObtainAuthToken):
    serializer_class = auth_serializers.LoginSerializer


    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token,created =Token.objects.get_or_create(user=user)

        chapter = None
        exco=None
        commitee = []
        if user.chapter:
            chapter={
                'name':user.chapter.name,
                'id':user.chapter.id
            }
        if user.user_type =='members':
            exco =user_models.ExcoRole.objects.filter(
                member= user.memeber
            ).values('name','id','chapter')
            commitee = user_models.CommiteeGroup.objects.filter(members=user.memeber).values('name','id')
        profile_image = ''
        try:
            profile_image = user.photo.url
        except:
            profile_image =''
        return Response({
            'token':token.key,'user_type':user.user_type,'chapter':chapter,'council':exco,'commitee':commitee,
            'userSecret':user.userSecret,
            'userName':user.userName,
            'user_id':user.id,
            'member_id': user.memeber.id if user.user_type=='members' else None,
            
            'profile_image':profile_image
            })


class UploadSecondLevelDataBaseView(CreateAPIView):
    serializer_class = auth_serializers.UploadSecondLevelDataBaseSerializer
    permission_classes =[IsAuthenticated,custom_permission.IsAdminOrSuperAdmin]


    def post(self, request, *args, **kwargs):
        serializedData = self.serializer_class(data=request.data)
        serializedData.is_valid(raise_exception=True)
        # activate the create function
        print(serializedData.save())
        return Success_response(msg="Database Created Successfully",data=[],status_code=status.HTTP_200_OK)



class ManageMemberValidation(viewsets.ViewSet):

    def list(self,request):
        "this would return list of validation Field"
        alum_db = auth_models.SecondLevelDatabase.objects.first()
        data = json.loads(alum_db.data)
        if not alum_db:
            raise CustomError({"error":"You have not uploaded the second level database"})
        # alum_db['useValidation'] this would return list of validations the admin has set already
        return Success_response(msg="Success",data=data['useValidation'],status_code=status.HTTP_200_OK)


    def create(self,request):

        valid_user = self._validateData(request)

        if valid_user:
            if valid_user.get('isValid')==True:
                return Success_response(msg="Success",data=[valid_user],status_code=status.HTTP_200_OK)
            else:return Success_response(msg="error",data=[valid_user],status_code=status.HTTP_400_BAD_REQUEST)

        raise CustomError({"error":"Validation UnSuccessfull"})

    def _validateData(self,request):
        """
        We would pass the request to this function that has data that contains same data we have in database
        e.g
        let say we have {'firstname':'matthew'} in reqquest.data and validation_list variable contains 'firstname' the fucntion will jsut check if we have the correct 
        value in data baseif yes  we return {'isValid':True,"user":valid_user}
        """
        # we return {isvalid:true,data:[]}
        alum_db = auth_models.SecondLevelDatabase.objects.first()
        data = json.loads(alum_db.data)
        users = data['usersInfo']
        validation_list = data['useValidation']
        frontEndData = request.data
        count=0
        valid_user =None
        try:
            for user in users:#we loop throug all the users
                for key in validation_list:#we get all the key we marked as --valid in the excel sheet
                    if frontEndData[key] == user[key]:#if the frontEndData is same with the database user 
                        count+=1#we add pluss one
                        if(count ==  len(validation_list)):#if the count matches the number of keys in validation_list then yes we have our self a valid_user
                            # print(user)
                            valid_user=user
                            break 

                count=0
            if valid_user:
                return {'isValid':True,"user":valid_user}
            else:
                return {'isValid':False,"user":None}
        except:
            raise CustomError('Wrong Validation Key')
    @action(detail=False,methods=['post'])
    def create_member(self,request, pk=None):
        """
        using this method just means we have our self valid user data 
        but here we pass  rel8Email->which is a email that would get the mail to activate and 'password' to create a valid memeber so they can login
        """
        alum_db = auth_models.SecondLevelDatabase.objects.first()
        alum_db =json.loads(alum_db.data)
        # password = 
        if not request.data.get('password'):
            raise CustomError({"password":"Password is missing"})
        if not request.data.get('rel8Email'):
            raise CustomError({"email":"Email is needed"})
        # if not request.data.get('alumni_year'):
        #     raise CustomError({"alumni_year":"alumni_year is needed"})
        password = request.data.pop('password')
        email = request.data.pop('rel8Email')
        alumni_year =  '2023-08-3'
        MEMBERSHIP_NO  = request.data.get('MEMBERSHIP_NO',None)
        if MEMBERSHIP_NO is None: raise CustomError({'error':'Please MEMBERSHIP_NO is missing'})
        if(self._validateData(request).get('isValid')==False):
            raise CustomError({"error":"Invalid Data"})
        
        if user_models.UserMemberInfo.objects.filter(value=MEMBERSHIP_NO).exists():
            raise CustomError({'error':'Membership info has been registered already'})
        chapter=None
        for key in request.data.keys():
            if key == 'chapter':
                chapter = request.data[key]  
        if chapter is None:
            raise CustomError({'error':'Chapter not found please reach out to admin'})
        if(len(alum_db['usersInfo'][0].keys())==len(request.data.keys())):
            if get_user_model().objects.filter(email=email).exists():raise CustomError({'error':'email already exists'})
            if not auth_models.Chapters.objects.filter(name__icontains=chapter):
                raise CustomError({'error':'chapter not found'})
            chapter_instance = auth_models.Chapters.objects.filter(name__icontains=chapter).first()
            user = get_user_model().objects.create_user(
                email=email,
                user_type='members',
                password =password,
                
            )
            user.chapter  = chapter_instance
            user.save()
            "we going to add chapters if there is"

            member = user_models.Memeber.objects.create(
                user =user,
                alumni_year=alumni_year
            )
            for key in request.data.keys():
                if not key =='password' and  not key == 'alumni_year':
                    user_models.UserMemberInfo.objects.create(
                        name= key,
                        value= request.data[key],
                        member=member
                    )
            mymailing_task.send_activation_mail.delay(user.id,user.email)
            # regiter_user_to_chat.delay(member.id)
            charge_new_member_dues.delay(user.id)
            
            return Success_response(msg="Success",data=[],status_code=status.HTTP_201_CREATED)
        raise CustomError({"error":"Data is not complete"})


class AdminManageCommiteeGroupViewSet(viewsets.ModelViewSet):
    """
        create view that manages the createiong of commitee and deletion,commitee,and postions 
    """
    serializer_class = auth_serializers.AdminManageCommiteeGroupSerializer
    permission_classes =[IsAuthenticated,custom_permission.IsAdminOrSuperAdmin]
    parser_classes = (custom_parsers.NestedMultipartParser,FormParser,)
    queryset = user_models.CommiteeGroup.objects.all()

    # @permission_classes([IsAuthenticated])

    @action(['get','post'],detail=False,permission_classes=[IsAuthenticated])
    def get_commitee(self,request,format=None):
        if request.method.lower() == 'get':
            if request.user.user_type in ['admin','super_admin']:
                all_commitee_group =self.queryset.all()
            else:
                all_commitee_group =self.queryset.filter(members__in=[request.user.memeber.id])
            clead_data = self.serializer_class(all_commitee_group,many=True)
        else:
            commitee_id = request.query_params.get('commitee_id',None)
            if commitee_id is None:raise CustomError({'error':'please provide commitee_id'})
            commitee = self.queryset.get(id=commitee_id)
            clead_data = self.serializer_class(commitee,many=False,context={'detail':True})
        return Success_response(msg="Success",data =clead_data.data)


    def create(self, request, *args, **kwargs):
        serialized_data = self.serializer_class(data=request.data)
        serialized_data.is_valid(raise_exception=True)
        committe_group =serialized_data.save()

        clean_data = self.serializer_class(committe_group)
        return Success_response(msg="Created Successfully",data=[clean_data.data],status_code=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        all_commitee_group =self.queryset.all()
        clead_data = self.serializer_class(all_commitee_group,many=True)
        print({
            'clead_data':clead_data.data
        })
        return Success_response(msg="Success",data =clead_data.data)

    @action(['post'],detail=False)
    def add_members(self,request,format=None):
        commitee_id = request.data.get('commitee_id',None)
        members_list = request.data.get('members_list',[])
        errors = []


        if not self.queryset.filter(id=commitee_id).exists():raise CustomError('Commitee does not exits')
       
        commitee = self.queryset.get(id=commitee_id)
        if request.query_params.get('clear_members',None) is not None:
            commitee.members.set([])
        else:
            for member_id in members_list:
                if not user_models.Memeber.objects.filter(id=member_id).exists():
                    errors.append([f"member with this id:'{member_id}' does not exits"])
                    # raise CustomError({'members_list':"this member doesn't exist"})
                else:
                    curentmember  =  user_models.Memeber.objects.get(id=member_id)
                    commitee.members.add(curentmember)


        


        clean_data = self.serializer_class(commitee)
        return Success_response(msg='added members successfully',data=[clean_data.data,{'errors':errors}])
    def partial_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        print({'pk':pk})
        if not self.queryset.filter(id=pk).exists():raise CustomError('Commitee does not exits')
        serialzed_data = self.serializer_class(instance=self.queryset.get(id=pk),data=request.data)
        serialzed_data.is_valid(raise_exception=True)
        updatedInstance = serialzed_data.save()
        clead_data = self.serializer_class(updatedInstance)
        return Success_response(msg='Updated',data=[clead_data.data])


class AdminManageCommiteeGroupPostionsViewSet(viewsets.ModelViewSet):
    serializer_class = auth_serializers.AdminManageCommiteePostion
    permission_classes =[IsAuthenticated,custom_permission.IsAdminOrSuperAdmin]
    queryset = user_models.CommiteePostion.objects.all()
    def create(self, request, *args, **kwargs):
        serialized = self.serializer_class(data=request.data)
        serialized.is_valid(raise_exception=True)
        updated_instance = serialized.save()
        clean_data = self.serializer_class(updated_instance)
        return Success_response('created successfull',data=[clean_data.data],status_code=status.HTTP_201_CREATED)


class SuperAdminMangeChapters(viewsets.ModelViewSet):
    "the super admin can create update the chapters"
    serializer_class = auth_serializers.ManageChapters
    permission_classes =[IsAuthenticated,custom_permission.IsSuperAdmin]
    queryset = auth_models.Chapters.objects.all()

    @action(detail=False,methods=['get'],permission_classes=[IsAuthenticated])
    def get_chapters(self,request, pk=None,):
        "any bodyu can list the chapters"

        return Success_response(msg="Success",data=[*self.queryset.values()])