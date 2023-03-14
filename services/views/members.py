from django.shortcuts import render
from  rest_framework import viewsets,response,status
from rest_framework import permissions
from utils.permissions import IsMember,IsMemberOwing
from services import models
from services.serialzer  import members  as serializer



class ReissuanceOfCertServicesViewSet(viewsets.ModelViewSet):
    queryset = models.ReissuanceOfCertServices.objects.all()
    permission_classes = [permissions.IsAuthenticated,IsMember,IsMemberOwing]
    serializer_class =serializer.ReissuanceOfCertCleaner

    def create(self, request, *args, **kwargs):
        serialized = serializer.ReissuanceOfCertSerializer(data=request.data,context={'member':self.request.user.memeber})
        serialized.is_valid(raise_exception=True)
        data = serialized.save()

        clean_data = serializer.ReissuanceOfCertCleaner(instance=data,many=False)

        return response.Response(data=clean_data.data,status=status.HTTP_201_CREATED)

class ChangeOfNameViewset(viewsets.ModelViewSet):
    queryset = models.ChangeOfName.objects.all()
    permission_classes = [permissions.IsAuthenticated,IsMember,IsMemberOwing]
    serializer_class = serializer.MemberChangeOfNameCleaner


    # def perform_create(self, serializer):
    #     serializer.save(member=self.request.user.memeber)

    def create(self, request, *args, **kwargs):
        serialized = serializer.MemberChangeOfNameSerializers(data=request.data,)
        serialized.is_valid(raise_exception=True)
        data = serialized.save(member=self.request.user.memeber)

        clean_data = serializer.MemberChangeOfNameCleaner(instance=data,many=False)

        return response.Response(data=clean_data.data,status=status.HTTP_201_CREATED)

class MemberLossOfCertificateServiceViewSet(viewsets.ModelViewSet):
    queryset = models.LossOfCertificateServices.objects.all()
    permission_classes = [permissions.IsAuthenticated,IsMember,IsMemberOwing]
    serializer_class = serializer.MemberLossOfCeriticateServiceCleaner

    def create(self, request, *args, **kwargs):
        serialized = serializer.MemberLossOfCertificateServicesSerializers(data=request.data,)
        serialized.is_valid(raise_exception=True)
        data = serialized.save(member=self.request.user.memeber)

        clean_data = serializer.MemberLossOfCeriticateServiceCleaner(instance=data,many=False)

        return response.Response(data=clean_data.data,status=status.HTTP_201_CREATED)


# 
    # def perform_create(self, serializer):
    #     serializer.save(member=self.request.user.memeber)



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
