from . import models
from rest_framework import serializers
from account.serializers.user import MemberSerializer


class PublicationParagraphSerializer(serializers.Serializer):
    paragragh = serializers.CharField(required=False)
    heading = serializers.CharField(required=False)

class AdminManagePublicationSerializer(serializers.ModelSerializer):

    paragraphs = serializers.SerializerMethodField()
    publication_paragraph = PublicationParagraphSerializer(many=True,write_only=True)


    def create(self, validated_data):
        publication_paragraph = validated_data.pop('publication_paragraph',[])
        publication =models.Publication.objects.create(**validated_data)
        for each_data in publication_paragraph:
            models.PublicationParagraph.objects.create(
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



class MemberCommentOnPublicationSerializer(serializers.ModelSerializer):

    member =  serializers.SerializerMethodField()
    
    # def get_member(self,publication_comment:models.PublicationComment):
    #     clean_data = MemberSerializer(instance=publication_comment.member,many=False)
    #     return clean_data.data

    def get_member(self,publication_comment:models.PublicationComment):
        user = publication_comment.member.user
        photo_url =''
        if user.photo:
            photo_url= user.photo.url

        full_name = publication_comment.member.full_name
        
        return {
            'full_name':full_name,
            'photo_url':photo_url,
            'id':publication_comment.member.id
        }
    def create(self, validated_data):
        data = super().create(validated_data)
        # clean_data =MemberCommentOnNewsSerializer(instance=data,many=False)
        return data
    class Meta:
        model = models.PublicationComment
        fields ='__all__'
        read_only_fields = ['member']