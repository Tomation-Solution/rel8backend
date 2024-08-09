import datetime 
import threading
import os

from rest_framework import serializers
from Rel8Tenant import models
from utils.custom_exceptions import CustomError
from django.db import connection, IntegrityError
from django.contrib.auth import get_user_model
from ..models import user as user_models
from account.models import auth as  user_auth_models
from django.shortcuts import get_object_or_404
from ..models import auth as auth_related_models
from account.serializers import user as user_related_serializer
from django.utils.encoding import force_str,force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from account.task import send_forgot_password_mail
User = get_user_model()
WEBSITEURL = os.environ['websiteurl']

def normalize_email(email):
    """
    Normalize the email address by lower-casing the domain part of it.
    """
    email = email or ''
    try:
        email_name, domain_part = email.strip().rsplit('@', 1)
    except ValueError:
        pass
    else:
        email = email_name + '@' + domain_part.lower()
    return email

class CreateAlumniSerializers(serializers.ModelSerializer):
    NameOfAlumni = serializers.CharField(required=True, write_only=True) 
    short_name_of_alumni = serializers.CharField(required=True, write_only=True)
    payment_plan = serializers.CharField(required=True, write_only=True)


    class Meta:
        model =models.Client
        fields =[
            "name",
            "paid_until",
            "on_trial",
            'created_at',
            'updated_at',
            "NameOfAlumni",'short_name_of_alumni','payment_plan','owner'
        ]
        
        read_only_fields = [
            "name",
            "paid_until",
            "on_trial",
            'created_at',
            'updated_at','owner'
        ]
    def validate(self, attrs):


        if(not attrs.get('payment_plan')):
            raise serializers.ValidationError({'payment_plan':'payment plan is required'})

        if(not attrs.get('NameOfAlumni')):
            raise serializers.ValidationError({"NameOfAlumni":'name_of_alumni  is required'})
        if(not attrs.get('short_name_of_alumni')):
            raise serializers.ValidationError({"short_name_of_alumni":"short_name_of_alumni is required"})
        return super().validate(attrs)

    def create(self, validated_data):
        print(validated_data)
        NameOfAlumni = validated_data.get('NameOfAlumni')
        short_name_of_alumni  = validated_data.get('short_name_of_alumni')
        payment_plan  = validated_data.get('payment_plan')
        loggedInUser = self.context.get('request').user
        
        

        try:
            tenant = models.Client.objects.create(
                name=NameOfAlumni,
                owner =normalize_email(loggedInUser.email),
                on_trial = True,
                payment_plan=payment_plan,
                schema_name=short_name_of_alumni,
                paid_until= datetime.datetime.today() + datetime.timedelta(days=365)
            )
            models.Domain.objects.create(
                # domain=f'{short_name_of_alumni}.{WEBSITEURL}',
                # we now using the subfolder instead of subdomain
                domain=short_name_of_alumni,
                tenant=tenant,
              is_primary=True
            )
            connection.set_schema(schema_name=short_name_of_alumni)
            User.objects.create_superuser(
                email = loggedInUser.email,
                password = loggedInUser.temp_password,)
            connection.set_schema(schema_name='public')
            return  tenant
        except IntegrityError as _:
            message = "value already exist"
            key = 'default'
            if 'email' or 'phone_number' in _.__str__():
                message = 'email already exists'
                # key = 'email'
            if 'phone_number' in _.__str__():
                message = 'phone_number already exists'
                # key = 'phone_number'
            print(message)
            print({"err":_})
            raise serializers.ValidationError({'key':_})
        # return super().create(validated_data)

class ExcoRoleSerializer(serializers.ModelSerializer):
    member = serializers.SerializerMethodField(read_only=True)

    def get_member(self, obj):
        return [member.name for member in obj.member.all()]

    class Meta:
        model = user_models.ExcoRole
        fields = '__all__'

class CreateExcoRole(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False)
    about = serializers.CharField(required=False)
    can_upload_min = serializers.BooleanField(required=False, default=False)
    member_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    is_remove_member = serializers.BooleanField(required=False, default=False)
    chapter_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        name = validated_data.get('name')
        about = validated_data.get('about')
        can_upload_min = validated_data.get('can_upload_min', False)
        chapter_id = validated_data.get('chapter_id')
        member_ids = validated_data.get('member_ids', [])

        chapter = None
        if self.context.get('request').user.user_type == 'admin':
            chapter = self.context.get('request').user.chapter

        if chapter_id:
            chapter = get_object_or_404(auth_related_models.Chapters, id=chapter_id)

        exco_role = user_models.ExcoRole.objects.create(
            name=name, about=about, can_upload_min=can_upload_min, chapter=chapter
        )
        for member_id in member_ids:
            member = get_object_or_404(user_models.Memeber, id=member_id)
            member.is_exco = True
            member.save()
            exco_role.member.add(member)

        exco_role.save()
        return exco_role

    def validate(self, attrs):
        member_ids = attrs.get('member_ids', [])
        for member_id in member_ids:
            if not user_models.Memeber.objects.filter(id=member_id).exists():
                raise CustomError({"error": f"Member with id {member_id} doesn't exist"})
        return super().validate(attrs)

    def update(self, instance, validated_data):
        member_ids = validated_data.get('member_ids', [])
        is_remove_member = validated_data.get('is_remove_member', False)
        new_chapter_instance = self.context.get('chapter')

        if is_remove_member:
            for member_id in member_ids:
                member = get_object_or_404(user_models.Memeber, id=member_id)
                member.is_exco = False
                member.save()
                instance.member.remove(member)
        else:
            for member_id in member_ids:
                member = get_object_or_404(user_models.Memeber, id=member_id)

                if instance.chapter is not None:
                    if member.user.chapter is None:
                        raise CustomError({"chapter": 'Member does not belong to a chapter yet'})
                    if instance.chapter.id != member.user.chapter.id:
                        raise CustomError({'chapter': f'Member does not belong to {instance.chapter.name} chapter'})

                member.is_exco = True
                member.save()
                instance.member.add(member)

        instance.name = validated_data.get('name', instance.name)
        instance.chapter = new_chapter_instance if new_chapter_instance else instance.chapter
        instance.about = validated_data.get('about', instance.about)
        instance.can_upload_min = validated_data.get('can_upload_min', instance.can_upload_min)

        instance.save()
        return instance

           


class CreateAnyAdminTypeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    chapters = serializers.CharField(required=False)

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        adminType =self.context.get('adminType')
        chapters= validated_data.get('chapters',None)
        if  user_models.User.objects.all().filter(email=email).exists():raise CustomError({"error":"User with this email exists"})
        if adminType == 'admin':
            
            "if it a admin chapters is required cus only a super admin can belong to a chapter"
            if chapters is None:
                raise CustomError({'chapter':'chapter is required to create a admin'})
            if not user_auth_models.Chapters.objects.filter(id=chapters).exists():
                raise CustomError({'chapter':'chapter does not exists'})
            chapters =  user_auth_models.Chapters.objects.get(id=chapters)
            user = user_models.User.objects.create_admin(
                email =email,password=password,
                **{"first_name":first_name,"last_name":last_name,'chapter':chapters}
                )
            user.save()

        if adminType == 'super_admin':
            user = user_models.User.objects.create_superuser(
                email =email,
                user_type=adminType,
                password=password,**{"first_name":first_name,"last_name":last_name}
                )
            user.save()


        return user

class MemberEmploymentHistorySerializerCleaner(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    is_delete = serializers.BooleanField(required=False)
    class Meta:
        model = user_models.MemberEmploymentHistory
        fields =[
            'member','postion_title','employment_from',
            'employment_to','employer_name_and_addresse','id','is_delete'
        ]
        read_only_fields=('member',)
class MemberEducationSerilizer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    is_delete = serializers.BooleanField(required=False)

    class Meta:
        model = user_models.MemberEducation
        fields = [
            'member','name_of_institution','major','degree',
            'language','reading','speaking','date','id','is_delete'
        ]  
        read_only_fields=('member',)

class MemberUpdateBioSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)
    membereducation = serializers.ListField(required=False)
    memberemploymenthistory = serializers.ListField(required=False)

    class Meta:
        model =user_models.Memeber
        fields= [
            'id',
            'amount_owing','is_exco','is_financial',
            'telephone_number','address','dob','citizenship',
            'memberemploymenthistory','membereducation'

        ]
        read_only_fields = ['amount_owing','is_exco','is_financial',]

    def create(self, validated_data):
        membereducation = validated_data.pop('membereducation',)
        Memberemploymenthistory = validated_data.pop('memberemploymenthistory',)
        member = self.context.get('user').memeber
        # for education in membereducation:
        #      education.pop('is_delete',None)
        #      user_models.MemberEducation.objects.create(**education,member=member)
            
        # for employment in Memberemploymenthistory:
        #     employment.pop('is_delete',None)
        #     user_models.MemberEmploymentHistory.objects.create(**employment,member=member)

        return member
    def update(self, instance, validated_data):
        # instance.telephone_number= validated_data.get('telephone_number',instance.telephone_number)
        # instance.address= validated_data.get('address',instance.address)
        # instance.dob= validated_data.get('dob',instance.dob)
        # instance.citizenship= validated_data.get('citizenship',instance.citizenship)
        instance.bio= validated_data.get('bio',instance.bio)
        instance.has_updated=True
        instance.save()
        membereducation = validated_data.get('membereducation',[])
        memberemploymenthistory = validated_data.get('memberemploymenthistory',[])
        
        for eduction in membereducation:
            if 'id' in eduction.keys():
                if user_models.MemberEducation.objects.filter(id=eduction['id']).exists():
                    member_education =user_models.MemberEducation.objects.get(id=eduction['id'])
                    if eduction.get('is_delete',False)==True:
                        member_education.delete()
                    else:
                        member_education.name_of_institution=eduction.get('name_of_institution',member_education.name_of_institution)
                        member_education.major=eduction.get('major',member_education.major)
                        member_education.degree=eduction.get('degree',member_education.degree)
                        member_education.language=eduction.get('language',member_education.language)
                        member_education.reading=eduction.get('reading',member_education.reading)
                        member_education.speaking=eduction.get('speaking',member_education.speaking)
                        member_education.date=eduction.get('date',member_education.date)
                        member_education.save()
            else:
                eduction.pop('is_delete',None)
                user_models.MemberEducation.objects.create(**eduction,member=instance)

        for employment in memberemploymenthistory:
            if 'id' in employment.keys():
                if user_models.MemberEmploymentHistory.objects.filter(id=employment['id']).exists():
                    member_employment =  user_models.MemberEmploymentHistory.objects.get(id=employment['id'])
                    if employment.get('is_delete'):
                        print('To be deleted',member_employment)
                        member_employment.delete()
                    else:
                        print('Updated',employment.get('is_delete'))
                        member_employment.postion_title = employment.get('postion_title',member_employment.postion_title)
                        member_employment.employment_from = employment.get('employment_from',member_employment.employment_from)
                        member_employment.employment_to = employment.get('employment_to',member_employment.employment_to)
                        member_employment.employer_name_and_addresse = employment.get('employer_name_and_addresse',member_employment.employer_name_and_addresse)
                        member_employment.save()
            else:
                employment.pop('member')
                employment.pop('is_delete',None)
                user_models.MemberEmploymentHistory.objects.create(**employment,member=instance)
        return instance


class HandleDeleteMemberBioSerializer(serializers.Serializer):
    memberemploymenthistory_ids = serializers.ListField(child=serializers.IntegerField())
    membereducation_ids = serializers.ListField(child=serializers.IntegerField())

    def create(self, validated_data):
        pass
    
class  RegisterUserToChapterView(serializers.Serializer):
    user_id = serializers.IntegerField()
    chapter_id =serializers.IntegerField()


    def create(self, validated_data):
        user_id = validated_data.get('user_id')
        chapter_id = validated_data.get('chapter_id')
        if not get_user_model().objects.filter(id=user_id).exists():
            raise CustomError({"error":"User Does Not exist"})
        if not user_auth_models.Chapters.objects.filter(id=chapter_id).exists():
            raise CustomError({"error":"Chapter Does Not exist"})

        user = get_user_model().objects.get(id=user_id)
        chapter = user_auth_models.Chapters.objects.get(id=chapter_id)
        if user.chapter is not None:
            raise CustomError({"error":"You already belong to a chapter"})
        user.chapter  = chapter
        user.save()
        return user


class MemberProfileUpdateSerializer(serializers.Serializer):
    name=  serializers.CharField()
    value=  serializers.CharField()
    id=  serializers.IntegerField()

    def create(self, validated_data):
        member_info_id = validated_data.get('id')
        user = self.context.get('user')
        if user_models.UserMemberInfo.objects.filter(id=member_info_id,member=user.memeber).exists():
            info = user_models.UserMemberInfo.objects.filter(id=member_info_id,member=user.memeber).first()
            info.value=validated_data.get('value',info.value)
            info.name=validated_data.get('name',info.name)
            info.save()
        return dict()


class MemberSerializer(serializers.ModelSerializer):

    member_info = serializers.SerializerMethodField()
    exco_info= serializers.SerializerMethodField()
    is_active =serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    photo =serializers.SerializerMethodField()
    member_education = serializers.SerializerMethodField()
    member_employment_history = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    def get_photo(self,member):
        user = member.user
        if user.photo:
            return user.photo.url
        else: return ''

    def get_member_education(self,member):
        eductation = user_models.MemberEducation.objects.filter(member=member)
        clean_data = MemberEducationSerilizer(instance=eductation,many=True)
        return clean_data.data
    def get_member_employment_history(self,member):
        employment = user_models.MemberEmploymentHistory.objects.filter(member=member)
        clean_data = MemberEmploymentHistorySerializerCleaner(instance=employment,many=True)

        return clean_data.data
    def get_is_active(self,member):return member.user.is_active

    def get_member_info(self,member):
        '#  this would return a list of the user member_info'
        return  user_models.UserMemberInfo.objects.filter(member=member.id).values()
    
    def get_email(self,member):return member.user.email
    def get_exco_info(self,member):
        '# if the user is a exco it would return list of the exco info else empty list'
        # if(member.is_exco==False): return []
        return user_models.ExcoRole.objects.filter(member=member.id).values()


    def get_full_name(self,member):
        return member.full_name
    
    class Meta:
        model = user_models.Memeber
        fields = '__all__'
        read_only_fields = ['id','member_info','email',
                            # 'member_education','member_employment_history',
                            'full_name','member_education','member_employment_history']

class IsOwningSerializerCleaner(serializers.ModelSerializer):
    email  = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()


    def get_photo(self,member):
        user = member.user
        if user.photo:
            return user.photo.url
        else: return ''
    def get_email(self,member):return member.user.email
    class Meta:
        model =user_models.Memeber
        fields = '__all__'


class UserProfilePicsSerializer(serializers.ModelSerializer):

    # def update(self, instance, validated_data):
    #     print(validated_data.get('photo'))
    #     instance.photo = validated_data.get('photo')
    #     instance.save()
    #     return ''

    class Meta:
        model = user_models.User
        fields = ['photo']


class userInfoSerializer(serializers.Serializer):
    name = serializers.CharField()
    value = serializers.CharField()
    id = serializers.IntegerField()


class AdminUpdateMemberInfoCleaner(serializers.Serializer):
    user_info = userInfoSerializer(many=True)

    # def update(self, instance, validated_data):
    #     user_info = validated_data.get('user_info')
        
    #     for eachinfo in user_info:
    #         user_models.UserMemberInfo.objects.filter(id=eachinfo.get('id')).update(value=eachinfo.get('value'))
    #     return dict()

    def update(self, instance, validated_data):
        user_info = validated_data.get('user_info')
        
        for eachinfo in user_info:
            user_member_info = user_models.UserMemberInfo.objects.filter(id=eachinfo.get('id')).first()
            if user_member_info:
                user_member_info.value = eachinfo.get('value')
                user_member_info.save()
        
        # Returning the instance to follow the convention of update methods
        return instance
    



class PasswordResetRequestSerializer(serializers.Serializer):
    email =  serializers.EmailField()
    def validate_email(self, email):
        User=get_user_model()
        if not User.objects.filter(email=email).exists():
            raise CustomError({'error':'User with this email address does not exist.'})
        return email
    
    def send_password_reset_email(self,user):
        # current_site = get_current_site(self.context['request'])
        uid=urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        domain ='app.sequentialjobs.com'
        reset_url = f"https://{connection.schema_name}.rel8membership.com/reset-password/{uid}/{token}/"
        if connection.schema_name == 'nimn':
            reset_url=f'https://members.nimn.com.ng/forgot-password/reset-password/{uid}/{token}/'
        if connection.schema_name =='test':
            reset_url = f'https://demo.rel8membership.com/reset-password/{uid}/{token}/'
        
        thread = threading.Thread(target=send_forgot_password_mail,args=[user.email,reset_url,connection.schema_name])
        thread.start()
        thread.join()
        
        # print({'reset_url':reset_url})
    def create(self, validated_data):
        user = get_user_model().objects.get(email=validated_data.get('email'))
        self.send_password_reset_email(user)
        return dict()
    
class PasswordResetConfirmationSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    token = serializers.CharField()
    uidb64 = serializers.CharField()

    def validate(self, attrs):
        User = get_user_model()
        try:
            uid =force_str(urlsafe_base64_decode(attrs['uidb64']))
            user = User.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise CustomError({'error':'Invalid reset password link.'})

        if not default_token_generator.check_token(user, attrs['token']):
            raise  CustomError({'error':'Invalid reset password link.'})

        attrs['user'] = user

        return attrs
    
    def save(self, **kwargs):
        user = self.validated_data['user']
        user.set_password(self.validated_data.get('new_password'))
        user.save()