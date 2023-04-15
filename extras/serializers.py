from rest_framework import serializers
from . import models




class GallerySerializer(serializers.ModelSerializer):


    class Meta:
        model = models.Gallery
        fields = "__all__"


class ImageStuff(serializers.Serializer):
    image  = serializers.ImageField()
    id = serializers.IntegerField()
class GalleryV2Serializer(serializers.ModelSerializer):
    images =serializers.SerializerMethodField()


    def get_images(self,galleryv2:models.GalleryV2):
        instance = models.ImagesForGalleryV2.objects.filter(gallery=galleryv2)

        clean_data =ImageStuff(instance,many=True)
        return clean_data.data
    class Meta:
        model = models.GalleryV2
        fields = "__all__"
        read_only_fields = ['images']


class AdminManageGalleryV2Serializer(serializers.ModelSerializer):
    upload_images =serializers.ListField(
        child= serializers.ImageField(max_length=10000000,allow_empty_file=False,use_url=False,write_only=True)
    )


    def create(self, validated_data):
        upload_images= validated_data.pop('upload_images')

        gallery = models.GalleryV2.objects.create(**validated_data)
        # ImagesForGalleryV2
        for image in upload_images:
            models.ImagesForGalleryV2.objects.create(
                image=image,
                gallery=gallery)
        return gallery

    class Meta:
        model = models.GalleryV2
        fields = ['name','date_taken','chapters','upload_images']



class TicketingSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.Ticketing
        fields = "__all__"





class AdminManagesProjectSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = models.FundAProject
        fields = ['heading','about','id','image','what_project_needs']



class MemberSupportProjectInKindSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SupportProjectInKind
        fields = ['heading','about','project']

class MemeberCustomerSupporSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CustomerSupport
        fields = ['heading','body','status','id']
        read_only_fields=['member','status','id',]