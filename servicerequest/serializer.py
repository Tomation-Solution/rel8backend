from rest_framework import serializers
from . import models


class MemberOfReissuanceOfCertificateSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.MemberOfReissuanceOfCertificate
        fields = '__all__'



class ChangeOfNameSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.ChangeOfName
        fields = '__all__'





class MergerOfCompaniesSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.MergerOfCompanies
        fields = '__all__'



class MergerOfCompaniesSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.MergerOfCompanies
        fields = '__all__'


class DeactivationOfMembershipSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.DeactivationOfMembership
        fields = '__all__'


class ProductManufacturingUpdateSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.ProductManufacturingUpdate
        fields = '__all__'



class FactoryLocationUpdateSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.FactoryLocationUpdate
        fields = '__all__'