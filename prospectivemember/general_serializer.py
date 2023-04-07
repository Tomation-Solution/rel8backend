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
        if not admin_rule.validate_keys(keys):
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