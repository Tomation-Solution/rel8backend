import requests
import json
from django.shortcuts import render
from rest_framework import viewsets,permissions
from utils import permissions as custom_permission
from utils.pagination import CustomPagination
from  . import models
from . import serializers
from utils.custom_response import Success_response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from . import filter as custom_filter
from utils import custom_parsers
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.parsers import  FormParser
from utils.usefulFunc import convert_naira_to_kobo
from utils.custom_exceptions import CustomError
from notifications.signals import notify



class GalleryView(viewsets.ModelViewSet):
    queryset = models.Gallery.objects.all()
    permission_classes = [permissions.IsAuthenticated,custom_permission.IsAdminOrSuperAdmin]
    serializer_class = serializers.GallerySerializer
    pagination_class=CustomPagination

    def create(self, request, *args, **kwargs):
        serialize = self.serializer_class(data=request.data,context={'request':request})
        serialize.is_valid(raise_exception=True)
        data = serialize.save()
        clean_data = self.serializer_class(data,many=False)

        return Success_response(msg="Success",data=[serialize.data],status_code=status.HTTP_200_OK)


    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(models.Gallery.objects.all())
        clean_data = self.serializer_class(page,many=True,context={'request':self.request})
        data= self.get_paginated_response(clean_data.data)

        # data  = self.get_paginated_response(clean_data.data)

        return Success_response(msg="Success",data=data,status_code=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(detail=False,methods=['get'],permission_classes=[custom_permission.IsMember])
    def member_get_gallery(self,request, pk=None):
        page = self.paginate_queryset(models.Gallery.objects.all())
        clean_data = self.serializer_class(page,many=True,context={'request':self.request})
        data= self.get_paginated_response(clean_data.data)
        return Success_response(msg="Success",data=data,status_code=status.HTTP_200_OK)



class GalleryV2View(viewsets.ModelViewSet):
    queryset= models.GalleryV2.objects.all()

    permission_classes = [permissions.IsAuthenticated,custom_permission.IsMember, permissions.AllowAny]
    serializer_class = serializers.GalleryV2Serializer
    pagination_class=CustomPagination
    filterset_class = custom_filter.GalleryV2Filter

    def list(self, request, *args, **kwargs):
        filter_set =custom_filter.GalleryV2Filter(request.query_params,queryset= self.get_queryset())
        page = self.paginate_queryset(filter_set.qs)
        clean_data = self.serializer_class(page,many=True,context={'request':self.request,'get_img':False})
        data= self.get_paginated_response(clean_data.data)
        #TODO: remove later
        notification_receiver = request.user
        notify.send(notification_receiver, recipient=notification_receiver, verb=f"{len(data)} folders received")
        return Success_response(msg="Success",data=data,status_code=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        gallery = get_object_or_404( models.GalleryV2,id=kwargs.get('pk',-1))
        clean_data = self.serializer_class(gallery,many=False,context={'request':self.request,'get_img':True})
        return Success_response(msg="Success",data=clean_data.data,status_code=status.HTTP_200_OK)

    
    @action(detail=False,methods=['get'],permission_classes=[permissions.AllowAny])
    def get_unauthorized_images(self,request, pk=None):
        paginated_pages = self.paginate_queryset(models.GalleryV2.objects.all())
        serialized_data = self.serializer_class(paginated_pages, many=True)
        paginated_data = self.get_paginated_response(serialized_data.data)
        return Success_response(msg="Success",data=paginated_data,status_code=status.HTTP_200_OK)


class GetUnAuthorizedGalleryFolder(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, pk): 
        gallery_instance = get_object_or_404(models.GalleryV2,id=pk)
        serializer = serializers.GalleryV2Serializer(gallery_instance,many=False)
        return Success_response(msg="Success",data=serializer.data,status_code=status.HTTP_200_OK)


class AdminManageGalleryV2View(GalleryV2View):
    queryset= models.GalleryV2.objects.all()

    permission_classes = [permissions.IsAuthenticated,custom_permission.IsAdminOrSuperAdmin]
    serializer_class = serializers.GalleryV2Serializer
    pagination_class=CustomPagination
    filterset_class = custom_filter.GalleryV2Filter

    def create(self, request, *args, **kwargs):
        serialzed = serializers.AdminManageGalleryV2Serializer(data=request.data)
        serialzed.is_valid(raise_exception=True)
        data = serialzed.save()
        clean_data = self.serializer_class(data)
        return Success_response(msg='Created',data=clean_data.data,status_code=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        name = request.data.get('name',None)
        id = kwargs.get('pk','-1')
        if name is None:
            raise CustomError({'error':'Please provide a name'})
        gallery = get_object_or_404(models.GalleryV2,id=id)
        gallery.name=name
        gallery.save()
        return Success_response(msg='Name Updated Successfully',data=[])

    @action(detail=False,methods=['post'],)
    def update_gallery_image(self,request,*args,**kwargs):
        image = request.data.get('image',None)
        id =  request.data.get('id','-1')
        if image is None:
            raise CustomError({'error':'Please provide an image'})
        galleyImage = get_object_or_404(models.ImagesForGalleryV2,id=id)
        galleyImage.image= image
        galleyImage.save()
        return Success_response('Updated Successfully',data=[])
    
class TicketingView(viewsets.ModelViewSet):
    queryset = models.Ticketing.objects.all()
    permission_classes = [permissions.IsAuthenticated,custom_permission.IsMember]
    serializer_class = serializers.TicketingSerializer


class AdminManagesProjectViewset(viewsets.ModelViewSet):
    serializer_class = serializers.AdminManagesProjectSerializer
    queryset = models.FundAProject.objects.all()
    permission_classes = [permissions.IsAuthenticated,custom_permission.IsAdminOrSuperAdmin]
    parser_classes = (custom_parsers.NestedMultipartParser,FormParser,)


class MemeberProjectSupportKindViewset(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated,custom_permission.IsMember]
    
    @action(detail=False,methods=['post'],)
    def support_in_kind(self, request, *args, **kwargs):
        serialzed = serializers.MemberSupportProjectInKindSerializer(data=request.data)
        serialzed.is_valid(raise_exception=True)
        data = serialzed.save(member=request.user.memeber)
        return Success_response(msg='Created',data=[],status_code=status.HTTP_201_CREATED)

    def list(self,request,*args,**kwargs):
        member_projects_instances = models.SupportProjectInKind.objects.filter(member__user=request.user)
        serializer = serializers.MemberSupportProjectInKindSerializer(instance=member_projects_instances,many=True)
        return Success_response(msg='Success',data=serializer.data,status_code=status.HTTP_200_OK)


class MemeberProjectSupportCashViewset(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated,custom_permission.IsMember]
    
    @action(detail=False,methods=['post'],)
    def support_in_cash(self, request, *args, **kwargs):
        serialzed = serializers.MemberSupportProjectInCashSerializer(data=request.data)
        serialzed.is_valid(raise_exception=True)
        data = serialzed.save(member=request.user.memeber)
        return Success_response(msg='Created',data=[],status_code=status.HTTP_201_CREATED)

    def list(self,request,*args,**kwargs):
        member_projects_instances = models.SupportProjectInCash.objects.filter(member__user=request.user)
        serializer = serializers.MemberSupportProjectInCashSerializer(instance=member_projects_instances,many=True)
        return Success_response(msg='Success',data=serializer.data,status_code=status.HTTP_200_OK)



class MemeberCustomerSupportViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,custom_permission.IsMember]
    queryset = models.CustomerSupport.objects.all()
    serializer_class = serializers.MemeberCustomerSupporSerializer

    def partial_update(self, request, *args, **kwargs):
        return False
    def update(self, request, *args, **kwargs):return False

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(member=self.request.user.memeber)

    def perform_create(self, serializer):
        serializer.save(member=self.request.user.memeber)



class MemberPersonalGallery(viewsets.ModelViewSet):
    queryset= models.MemberPersonalGallery.objects.all()
    permission_classes = [permissions.IsAuthenticated,custom_permission.IsMember]
    serializer_class = serializers.MemberPersonalGallerySerializer

    def get_queryset(self):
        return models.MemberPersonalGallery.objects.filter(member=self.request.user.memeber)


    def perform_create(self, serializer):
        serializer.save(member=self.request.user.memeber)


class FundAProjectPayment(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,*args, **kwargs):
        """ request data
            {
                "amount": 0,
                "project_id": 1,
                "member_remark": ""
            }
        """
        
        url = 'https://api.paystack.co/transaction/initialize/'
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET}',
            'Content-Type' : 'application/json',
            'Accept': 'application/json'
        }
        body = {
            "email": request.user.email,
            "amount": convert_naira_to_kobo(request.data.get('amount')),
            "metadata":{
                'project_id': request.data.get('project_id'),
                "user_id":request.user.id,
                "member_remark": request.data.get('member_remark'),
                "is_paid": True
            },
            "callback_url": settings.PAYMENT_FOR_PROJECT_CALLBACK,
            }
        try:
            response = requests.post(url,headers=headers,data=json.dumps(body))
        except requests.ConnectionError:
            raise CustomError({"error":"Network Error"},status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
  
        if  response.status_code in  [200, 201]:
            return Success_response(msg='Payment processing in progress!',data=response.json())

        raise CustomError(message={"error":'Some error occured please try again'},status_code=status.HTTP_503_SERVICE_UNAVAILABLE)