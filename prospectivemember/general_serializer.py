from rest_framework import serializers
from .models import general as general_models
from account.models import User
from utils.custom_exceptions import CustomError
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
        admin_rule = general_models.AdminSetPropectiveMembershipRule.objects.all().first()
        if admin_rule is None:
            raise CustomError({'error':'please reach out to your admin to set text_fields'})
        data =attrs.get('data')
        keys = map(lambda eachData: eachData.get('name'),data)
        if not admin_rule.validate_text_fields_keys(keys):
            raise CustomError({'error':'in complete data'})
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
        data =attrs.get('data')
        keys = attrs.keys()
        if not admin_rule.validate_file_fields_keys(keys):
            raise CustomError({'error':'in complete data'})


    def create(self, validated_data):
        prospective_member= self.context.get('user').prospectivememberprofile

        form,_= general_models.ProspectiveMemberFormTwo.objects.get_or_create(
            prospective_member=prospective_member,)
        keys =validated_data.keys()
        for key in keys:
            general_models.ProspectiveMemberFormTwoFile.objects.create(
                name=key,
                file=validated_data[key],
                form_two=form
            )
        return dict()
 