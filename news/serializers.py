from . import models
from rest_framework import serializers




class AdminManageNewSerializer(serializers.ModelSerializer):


    paragraphs = serializers.SerializerMethodField()
    has_reacted = serializers.SerializerMethodField()


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

