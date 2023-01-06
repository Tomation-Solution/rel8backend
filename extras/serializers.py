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





class TicketingSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.Ticketing
        fields = "__all__"


