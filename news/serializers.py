from . import models
from rest_framework import serializers



class NewsParagraphSerializer(serializers.Serializer):
    paragragh = serializers.CharField(required=False)
    heading = serializers.CharField(required=False)
class AdminManageNewSerializer(serializers.ModelSerializer):


    paragraphs = serializers.SerializerMethodField()
    has_reacted = serializers.SerializerMethodField()

    news_paragraph = NewsParagraphSerializer(many=True,write_only=True)

    def create(self, validated_data):
        news_paragraph = validated_data.pop('news_paragraph',[])
        news =models.News.objects.create(**validated_data)
        for each_data in news_paragraph:
            models.NewsParagraph.objects.create(
                news= news,
                paragragh=each_data.get('paragragh',None),
                heading=each_data.get('heading',None),
            )
        return news

    def get_has_reacted(self,news):
        request = self.context.get('request')
        if request.user.user_type in ['admin','super_admin']:return False
        return news.id==request.user.memeber.id

    def get_paragraphs(self,news):

        return models.NewsParagraph.objects.filter(news=news,).values('id','paragragh','heading')
    def update(self, instance, validated_data):

        instance.likes = validated_data.get('likes',instance.likes)
        instance.dislikes = validated_data.get('dislikes',instance.dislikes)
        instance.save()
        return instance
    class Meta:
        model = models.News
        fields = "__all__"

