from . import models
from rest_framework import serializers
from account.models.user import UserMemberInfo
from account.serializers.user import MemberSerializer


class NewsParagraphSerializer(serializers.Serializer):
    paragragh = serializers.CharField(allow_blank=True)
    heading = serializers.CharField(allow_blank=True)
class AdminManageNewSerializer(serializers.ModelSerializer):
    # write = serializers.SerializerMethodField()
    paragraphs = serializers.SerializerMethodField()
    has_reacted = serializers.SerializerMethodField()

    news_paragraph = NewsParagraphSerializer(many=True,write_only=True,)

    # def get_writer(self, obj):
    #     return f"{obj.writer.first_name} {obj.writer.last_name}"

    def create(self, validated_data):
        news_paragraph = validated_data.pop('news_paragraph',[])
        news =models.News.objects.create(**validated_data)
        for each_data in news_paragraph:
            models.NewsParagraph.objects.create(
                news= news,
                paragragh=each_data.get('paragragh',' '),
                heading=each_data.get('heading',' '),
            )
        return news

    def get_has_reacted(self,news):
        request = self.context.get('request')
        if request.user.user_type in ['admin','super_admin']:return False
        return news.id==request.user.memeber.id

    def get_paragraphs(self,news):

        return models.NewsParagraph.objects.filter(news=news,).values('id','paragragh','heading')
    def update(self, instance, validated_data):
        # is_liked = validated_data.get('likes')
        # is_disliked = validated_data.get('dislikes')

        # if is_liked:
        #     instance.likes += 1

        # if is_disliked:            
        #     instance.dislikes += 1

        # instance.save()
        # return instance
        pass

    class Meta:
        model = models.News
        fields = "__all__"


class MemberCommentOnNewsSerializer(serializers.ModelSerializer):

    member =  serializers.SerializerMethodField()
    
    def get_member(self,news_comment:models.NewsComment):
        user = news_comment.member.user
        photo_url =''
        if user.photo:
            photo_url= user.photo.url

        full_name = news_comment.member.full_name
        
        return {
            'full_name': full_name,
            'photo_url':photo_url,
            'id':news_comment.member.id
        }

    def create(self, validated_data):
        data = super().create(validated_data)
        # clean_data =MemberCommentOnNewsSerializer(instance=data,many=False)
        return data
    class Meta:
        model = models.NewsComment
        fields ='__all__'
        read_only_fields = ['member']