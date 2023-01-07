from . import models
from rest_framework import serializers


class PublicationParagraphSerializer(serializers.Serializer):
    paragragh = serializers.CharField(required=False)
    heading = serializers.CharField(required=False)

class AdminManagePublicationSerializer(serializers.ModelSerializer):

    paragraphs = serializers.SerializerMethodField()
    publication_paragraph = PublicationParagraphSerializer(many=True,write_only=True)


    def create(self, validated_data):
        publication = validated_data.pop('publication_paragraph',[])
        publication =models.Publication.objects.create(**validated_data)
        for each_data in news_paragraph:
            models.Publication.objects.create(
                publication= publication,
                paragragh=each_data.get('paragragh',None),
                heading=each_data.get('heading',None),
            )
        return publication
        
    def get_paragraphs(self,publication):
        return models.PublicationParagraph.objects.filter(publication=publication,).values('id','paragragh','heading')
    def update(self, instance, validated_data):

        instance.likes = validated_data.get('likes',instance.likes)
        instance.dislikes = validated_data.get('dislikes',instance.dislikes)
        instance.save()
        return instance
    class Meta:
        model = models.Publication
        fields = "__all__"

