from django.shortcuts import render
from  rest_framework import viewsets
from rest_framework import permissions
from utils.permissions import IsMember,IsMemberOwing
from services import models
from services.serialzer  import members  as serializer



class ChangeOfNameViewset(viewsets.ModelViewSet):
    queryset = models.ChangeOfName.objects.all()
    permission_classes = [permissions.IsAuthenticated,IsMember,IsMemberOwing]
    serializer_class = serializer.MemberChangeOfNameSerializers


    def perform_create(self, serializer):
        serializer.save(member=self.request.user.memeber)


class MemberLossOfCertificateServiceViewSet(viewsets.ModelViewSet):
    queryset = models.LossOfCertificateServices.objects.all()
    permission_classes = [permissions.IsAuthenticated,IsMember,IsMemberOwing]
    serializer_class = serializer.MemberLossOfCertificateServicesSerializers


    def perform_create(self, serializer):
        serializer.save(member=self.request.user.memeber)



class DeactivationOfMembershipViewset(viewsets.ModelViewSet):
    queryset = models.DeactivationOfMembership.objects.all()
    permission_classes = [permissions.IsAuthenticated,IsMember,IsMemberOwing]
    serializer_class = serializer.MemberDeactivationOfMembershipSerializer


    def perform_create(self, serializer):
        serializer.save(member=self.request.user.memeber)


class ProductManufacturingUpdateViewset(viewsets.ModelViewSet):
    queryset = models.UpdateOnProductsManufactured.objects.all()
    permission_classes = [permissions.IsAuthenticated,IsMember,IsMemberOwing]
    serializer_class = serializer.UpdateOnProductsManufacturedSerializer


    def perform_create(self, serializer):
        serializer.save(member=self.request.user.memeber)

class ActivationOfDeactivatedMemberViewSet(viewsets.ModelViewSet):
    queryset = models.ActivationOfDeactivatedMember.objects.all()
    permission_classes = [permissions.IsAuthenticated,IsMember,IsMemberOwing]
    serializer_class = serializer.MemberActivationOfDeactivatedMemberSerializer


    def perform_create(self, serializer):
        serializer.save(member=self.request.user.memeber)
