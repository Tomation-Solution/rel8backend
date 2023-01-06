from cProfile import run
from rest_framework import serializers

from utils.custom_exceptions import CustomError
from . import models
from account.models import auth as auth_related_models
from account.models import user as user_related_models





class DueCleanSerialier(serializers.ModelSerializer):
    chapter = serializers.SerializerMethodField()
    
    def get_chapter(self,due):
        if(due.chapters): return {
            'name':due.chapters.name,
            'id':due.chapters.id,
        }
        return None
    class Meta:
        model = models.Due
        fields = [
             "Name",
            "re_occuring",
            "is_for_excos",
            "amount",
            "startDate",
            "startTime",
            "endDate",
            "scheduletype",
            "schedule",
            'chapter','id'
        ]

class AdminManageDuesSerializer(serializers.Serializer):
    name = serializers.CharField()
    re_occuring = serializers.BooleanField()
    is_for_excos = serializers.BooleanField()
    amount = serializers.FloatField()
    startDate = serializers.DateField(
          format="%d-%m-%Y",
        input_formats=["%d-%m-%Y", "iso-8601"],
        required=True,
    )
    startTime = serializers.TimeField()
    scheduletype = serializers.CharField(required=False)#day_of_week or month_of_year
    schedule = serializers.ListField(required=False)
    alumni_year= serializers.DateField(required=True,)
    # alumni_year

    # for_chapters=serializers.BooleanField(default=False,)


    def check_schedule(value_list):
        "let check if it all contains str" 
        for value  in  value_list:
            if(not isinstance(value,str)):
                raise serializers.ValidationError({"error":'schedule must contain string of numbers'})
            
            if(isinstance(value,str)):
                try:
                    int(value)
                except ValueError:
                    raise serializers.ValidationError({"error":'schedule must contain string of numbers not letter'})
        return value_list
            
    def validate(self, attrs):
        # self.check_schedule()
        re_occuring = attrs.get('re_occuring',None)
        scheduletype= attrs.get('scheduletype',None)
        schedule= attrs.get('schedule',None)
        if re_occuring:
            "if it re_occuring we need some of this fields"
            if(scheduletype is None):
                raise serializers.ValidationError({'scheduletype':'this is re_occuring, it should be either day_of_week or month_of_year'})
            if(not(scheduletype =='day_of_week' or scheduletype =='month_of_year')):
                raise serializers.ValidationError({'scheduletype':'this is re_occuring, it should be either day_of_week or month_of_year'})
            if(not isinstance(schedule,list)):
                raise serializers.ValidationError({'schedule':'must be a list'})
        return super().validate(attrs)


    def create(self, validated_data):
        # for_chapters=validated_data.pop('for_chapters',None)
        user = self.context.get('request').user
        chapter=None
        if user.user_type in ['admin']:#this means if he is an admin we force him to create for only this chapter
            chapter = auth_related_models.Chapters.objects.get(id=user.chapter.id)
        if user.user_type in ['super_admin']:
            'this means this person wants to create National Event he must be a super admin'
            chapter=None
            # if not user_related_models.Super_admin.objects.all().filter(user=user).exists():
            #     "if this user is not a super admin there is a problem he cant create a national event"
            #     raise CustomError({"error":"You can't Create A national Event"})

        name = validated_data.get('name')
        re_occuring = validated_data.get('re_occuring')
        is_for_excos = validated_data.get('is_for_excos')
        amount = validated_data.get('amount')
        startDate = validated_data.get('startDate')
        startTime =  validated_data.get('startTime')
        scheduletype =  validated_data.get('scheduletype','day_of_week')
        schedule =   validated_data.get('schedule',['0'])
        alumni_year = validated_data.get('alumni_year',None)
        if models.Due.objects.filter(Name=name).exists():raise serializers.ValidationError({"error":'Due name exists already'})
        due = models.Due.objects.create(
            Name =name,
        re_occuring = re_occuring,
        is_for_excos = is_for_excos,
        amount =amount,
        startDate =startDate,
        startTime =  startTime,
        scheduletype = scheduletype,
        schedule =   schedule,chapters=chapter,
        alumni_year=alumni_year
        )
        due.chapters=chapter
        due.save()
        # print(validated_data)
        return due.id
        




class AdminManageDeactivatingDuesSerializer(serializers.Serializer):
    name = serializers.CharField()
    is_for_excos = serializers.BooleanField()
    amount = serializers.FloatField()
    month = serializers.IntegerField()
    startDate = serializers.DateField(
    format="%d-%m-%Y",
    input_formats=["%d-%m-%Y", "iso-8601"],
    required=True,
    )
    startTime = serializers.TimeField()
    # for_chapters=serializers.BooleanField(default=False,)


    def create(self, validated_data):
        for_chapters=validated_data.pop('for_chapters',None)
        user = self.context.get('request').user
        chapter = None
        if  user.user_type in ['admin']:
            chapter = auth_related_models.Chapters.objects.get(id=user.chapter.id)
        if  user.user_type in ['super_admin']:
            'this is a super admin that has the right only to create a National due'
            chapter = None

            # if not user_related_models.Super_admin.objects.all().filter(user=user).exists():
            #     "if this user is not a super admin there is a problem he cant create a national event"
            #     raise CustomError({"error":"You can't Create A national Event"})



        name = validated_data.get('name')
        is_for_excos = validated_data.get('is_for_excos')
        amount = validated_data.get('amount')
        startDate = validated_data.get('startDate')
        startTime =  validated_data.get('startTime')
        month =   validated_data.get('month')
        if month == 0:
            raise serializers.ValidationError({"name":'must be 1 or more'})
        if models.DeactivatingDue.objects.filter(name=name).exists():raise serializers.ValidationError({"name":'Deactivating Due name exists already'})

        due = models.DeactivatingDue.objects.create(
            name =name,
            is_for_excos = is_for_excos,
            amount =amount,
            startDate =startDate,
            startTime =  startTime,
            month =   str(month),chapters=chapter)
        due.save()
        return due.id
