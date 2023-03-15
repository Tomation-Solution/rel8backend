from django.shortcuts import render
from  rest_framework import viewsets,response,status as status_code
from rest_framework import permissions
from utils.permissions import IsAdminOrSuperAdmin
from services import models
from services.serialzer  import members  as memeber_serializer
from rest_framework.decorators import action

class ChangeStatus:

    @action(methods=['post'],detail=False,)
    def update_status(self,request,*args,**kwargs):
        instance_id = request.data.get('id',-1)
        status = request.data.get('status','pending')
        instance = self.queryset.get(id=instance_id)
        instance.status=status
        instance.save()
        data = self.serializer_class(instance=instance,)
        return response.Response(data=data.data,status=status_code.HTTP_200_OK)

class AdminManageChangeOfNameView(viewsets.ModelViewSet,ChangeStatus):
    queryset = models.ChangeOfName.objects.all()
    permission_classes = [permissions.IsAuthenticated,IsAdminOrSuperAdmin,]
    serializer_class=memeber_serializer.MemberChangeOfNameCleaner

    permission_classes = [permissions.IsAuthenticated,IsAdminOrSuperAdmin,]


class AdminLossOfCertificateServiceViewSet(viewsets.ModelViewSet,ChangeStatus):
    queryset = models.LossOfCertificateServices.objects.all()
    serializer_class = memeber_serializer.MemberLossOfCeriticateServiceCleaner
    permission_classes = [permissions.IsAuthenticated,IsAdminOrSuperAdmin,]



class AdminDeactivationOfMembershipViewset(viewsets.ModelViewSet,ChangeStatus):
    queryset = models.DeactivationOfMembership.objects.all()
    serializer_class = memeber_serializer.MemberDeactivationOfMembershipSerializer
    permission_classes = [permissions.IsAuthenticated,IsAdminOrSuperAdmin,]


class AdminProductManufacturingUpdateViewset(viewsets.ModelViewSet,ChangeStatus):
    queryset = models.UpdateOnProductsManufactured.objects.all()
    serializer_class = memeber_serializer.UpdateOnProductsManufacturedSerializer
    permission_classes = [permissions.IsAuthenticated,IsAdminOrSuperAdmin,]


class AdminActivationOfDeactivatedMemberViewSet(viewsets.ModelViewSet,ChangeStatus):
    queryset = models.ActivationOfDeactivatedMember.objects.all()
    serializer_class = memeber_serializer.MemberActivationOfDeactivatedMemberSerializer
    permission_classes = [permissions.IsAuthenticated,IsAdminOrSuperAdmin,]
