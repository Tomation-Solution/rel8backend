from rest_framework import serializers
from .models import general as general_models
from account.models import User
from utils.custom_exceptions import CustomError
from django.core.files import File

class CreatePropectiveMemberSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    

    class Meta:
        model = general_models.ProspectiveMemberProfile
        read_only_fields =['user','id','amount_paid','paystack','has_paid']
        fields = '__all__'

    def validate(self, attrs):
        if User.objects.filter(email=attrs.get('email')).exists():
            raise CustomError({'error':'email already exist'})
        return super().validate(attrs)
    
    def create(self, validated_data):
        email =   validated_data.get('email')
        password= validated_data.pop('password')

        user = User.objects.create_user(email=email,password=password,user_type='prospective_members')    
        user.is_prospective_Member=True
        user.save()

        prospectiveMember = general_models.ProspectiveMemberProfile.objects.create(
            user = user,**validated_data)
        return prospectiveMember
    
    def update(self, instance, validated_data):
        return dict()



class  PropectiveMemberFormOneAllInfoSerializer(serializers.Serializer):
    name =serializers.CharField()
    value = serializers.CharField()
class PropectiveMemberFormOneSerializer(serializers.Serializer):
    data= PropectiveMemberFormOneAllInfoSerializer(many=True)


    def validate(self, attrs):
        # admin_rule = general_models.AdminSetPropectiveMembershipRule.objects.all().first()
        # if admin_rule is None:
        #     raise CustomError({'error':'please reach out to your admin to set text_fields'})
        # data =attrs.get('data')
        # keys = map(lambda eachData: eachData.get('name'),data)
        # if not admin_rule.validate_text_fields_keys(keys):
        #     raise CustomError({'error':'in complete data'})
        return super().validate(attrs)
 
    def create(self, validated_data):
        data =validated_data.get('data')
        prospective_member= self.context.get('user').prospectivememberprofile
        form,_ = general_models.ProspectiveMemberFormOne.objects.get_or_create(
            prospective_member=prospective_member,)
        form.info=data
        form.save()
        
        return form
    
class PropectiveMemberFormOneCleaner(serializers.ModelSerializer):

    class Meta:
        model = general_models.ProspectiveMemberFormOne
        fields = '__all__'
class ProspectiveMemberFormTwoFileCleaner(serializers.ModelSerializer):

    class Meta:
        model = general_models.ProspectiveMemberFormTwoFile
        fields = '__all__'

class PropectiveMemberFormTwoCleaner(serializers.ModelSerializer):
    files = serializers.SerializerMethodField()

    def get_files(self,instance):
        data =general_models.ProspectiveMemberFormTwoFile.objects.filter(form_two=instance)
        clean_data =ProspectiveMemberFormTwoFileCleaner(instance=data,many=True)
        return  clean_data.data
    class Meta:
        model = general_models.ProspectiveMemberFormTwo
        fields = '__all__'



class PropectiveMemberFormTwoSerializerUpdate:
    'this is a custom serializer '
    """
        NOTE steps of data flow

        first of how the data is going to look like this -> idOfImg:actualmage
        second i call a validate function to check all the ids if they are actually exist and if the logged in user owns them
        after the validation get passed
        third step we use the id to update the images(final stage)
    """

    def __init__(self,data,context=dict()):
        self.data= data
        self.context = context
        self.validate()
        self.update()


    def update(self):
        keys = self.data.keys()
        # all_files = general_models.ProspectiveMemberFormTwoFile.objects.filter(id__in=keys)
        for key in keys:
             instance = general_models.ProspectiveMemberFormTwoFile.objects.filter(
                 id=key).first()
             if instance:
                serializer =ProspectiveMemberFormTwoFileCleaner(instance=instance,data={'file':self.data.get(key)},partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            #  .update(
            #      file=self.data.get(key).file)
        return self.data

        pass
    def validate(self,):
        admin_rule = general_models.AdminSetPropectiveMembershipRule.objects.all().first()
        if admin_rule is None:
            raise CustomError({'error':'please reach out to your admin to set text_fields'})
        keys = self.data.keys()

        all_files = general_models.ProspectiveMemberFormTwoFile.objects.filter(id__in=keys)
        if not general_models.ProspectiveMemberFormTwoFile.objects.filter(id__in=keys).exists():
            raise CustomError({'error':'please check what you updating'})
        
        all_files = all_files.first()
        if all_files.form_two.prospective_member.user.id != self.context.get('user').id:
            raise CustomError({'error':'unauthorised'})

class PropectiveMemberFormTwoSerializer:
    'custom serialzer'
    """
    Flow of data
    for create
        first we take any data from here 
        filename:   actualFile
        once it get to the validate fucntion we check if the keys are same with what the admin has set
        then we use some algorithm to some how uplaod it without us knowing the keys
    for update:
        they would only be able to updaate one file at a time ...
    """

    def __init__(self,data,context=dict()):
        self.data = data
        self.context = context

        self.validate(data)
        self.create(data)
    def validate(self, attrs)->None:
        admin_rule = general_models.AdminSetPropectiveMembershipRule.objects.all().first()
        if admin_rule is None:
            raise CustomError({'error':'please reach out to your admin to set text_fields'})
        # data =attrs.get('data')
        # keys = attrs.keys()
        # if not admin_rule.validate_file_fields_keys(keys):
        #     raise CustomError({'error':'in complete data'})


    def create(self, validated_data):
        prospective_member= self.context.get('user').prospectivememberprofile

        form,_= general_models.ProspectiveMemberFormTwo.objects.get_or_create(
            prospective_member=prospective_member,)
        keys =validated_data.keys()
        print({'validated':validated_data})
        for key in keys:
            fileFormInstance,_ = general_models.ProspectiveMemberFormTwoFile.objects.get_or_create(
                name=key,
                form_two=form
            )
            fileFormInstance.file=validated_data[key]
            fileFormInstance.save()
        return dict()
 

class ProspectiveMemberFormTwoFileSerailzer(serializers.ModelSerializer):

    

    class Meta:
        model = general_models.ProspectiveMemberFormTwoFile
        fields= '__all__'
        read_only_fields=['form_two','name','id']


class AdminManageProspectiveRuleSerializer(serializers.ModelSerializer):

    

    class Meta:
        model=general_models.AdminSetPropectiveMembershipRule
        fields = '__all__'

class ProspectiveMemberFormTwoFileCleaner(serializers.ModelSerializer):

    class Meta:
        model=general_models.ProspectiveMemberFormTwoFile
        fields ='__all__'

class ProspectiveMemberCleaner(serializers.ModelSerializer):
    form_one = serializers.SerializerMethodField()
    form_two = serializers.SerializerMethodField()
    def get_form_one(self,instance: general_models.ProspectiveMemberProfile):
        form_one,_ = general_models.ProspectiveMemberFormOne.objects.get_or_create(prospective_member=instance)
        return {
            'id':form_one.id,
            'info':form_one.info,
        }
    def get_form_two(self,instance):
        form_two,_ = general_models.ProspectiveMemberFormTwo.objects.get_or_create(prospective_member=instance)
        data =general_models.ProspectiveMemberFormTwoFile.objects.filter(form_two=form_two)
        clen_data =ProspectiveMemberFormTwoFileCleaner(instance=data,many=True)
        return clen_data.data
    class Meta:
        model = general_models.ProspectiveMemberProfile
        fields = '__all__'
