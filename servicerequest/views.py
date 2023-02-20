from django.shortcuts import render
from . import models
from rest_framework import viewsets
from utils.permissions import IsMember
from rest_framework import permissions
from . import serializer
# Create your views here.


class MemberOfReissuanceOfCertificateViewset(viewsets.ModelViewSet):
    queryset = models.MemberOfReissuanceOfCertificate.objects.all()
    permission_classes = [permissions.IsAuthenticated,IsMember]
    serializer_class = serializer.MemberOfReissuanceOfCertificateSerializer


class ChangeOfNameViewset(viewsets.ModelViewSet):
    queryset = models.ChangeOfName.objects.all()
    permission_classes = [permissions.IsAuthenticated,IsMember]
    serializer_class = serializer.ChangeOfNameSerializer


class MergerOfCompaniesViewset(viewsets.ModelViewSet):
    queryset = models.MergerOfCompanies.objects.all()
    permission_classes = [permissions.IsAuthenticated,IsMember]
    serializer_class = serializer.MergerOfCompaniesSerializer

class DeactivationOfMembershipViewset(viewsets.ModelViewSet):
    queryset = models.DeactivationOfMembership.objects.all()
    permission_classes = [permissions.IsAuthenticated,IsMember]
    serializer_class = serializer.DeactivationOfMembershipSerializer

class ProductManufacturingUpdateViewset(viewsets.ModelViewSet):
    queryset = models.ProductManufacturingUpdate.objects.all()
    permission_classes = [permissions.IsAuthenticated,IsMember]
    serializer_class = serializer.ProductManufacturingUpdateSerializer


class FactoryLocationUpdateViewset(viewsets.ModelViewSet):
    queryset = models.FactoryLocationUpdate.objects.all()
    permission_classes = [permissions.IsAuthenticated,IsMember]
    serializer_class = serializer.FactoryLocationUpdateSerializer