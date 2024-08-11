from rest_framework import serializers

class ContactUsSerializer(serializers.Serializer):

    sender_name = serializers.CharField(max_length=100)
    sender_email = serializers.EmailField()
    message = serializers.CharField()