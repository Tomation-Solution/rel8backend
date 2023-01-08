from rest_framework import serializers
from . import models




class GallerySerializer(serializers.ModelSerializer):


    class Meta:
        model = models.Gallery
        fields = "__all__"



class GalleryV2Serializer(serializers.ModelSerializer):
    images =serializers.SerializerMethodField()


    def get_images(self,galleryv2:models.GalleryV2):
        get_img  = self.context.get('get_img',True)
        if get_img: 
            return models.ImagesForGalleryV2.objects.filter(gallery=galleryv2).values('image')
        return []
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


