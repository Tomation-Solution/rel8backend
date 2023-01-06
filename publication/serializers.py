from . import models
from rest_framework import serializers




class AdminManagePublicationSerializer(serializers.ModelSerializer):

    paragraphs = serializers.SerializerMethodField()

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

