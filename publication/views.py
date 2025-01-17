from django.shortcuts import render
from rest_framework import viewsets,permissions,views,status

from utils.custom_exceptions import CustomError
from . import models
from rest_framework.views import APIView
from utils import permissions as custom_permission
from . import serializers,filter as custom_filter
from account.models import user as user_related_models
from utils import custom_response,custom_parsers
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

class AdminManagePublication(viewsets.ModelViewSet):
    queryset = models.Publication.objects.all()
    permission_classes = [permissions.IsAuthenticated, custom_permission.IsAdminOrSuperAdmin, custom_permission.Normal_Admin_Must_BelongToACHapter]
    serializer_class = serializers.AdminManagePublicationSerializer
    parser_classes = (custom_parsers.NestedMultipartParser, FormParser,)

    def create(self, request, format=None):
        'create Publication'
        serialize = self.serializer_class(data=request.data, context={"request": request})
        serialize.is_valid(raise_exception=True)
        instance = serialize.save()
        if self.request.user.user_type == 'admin':
            # Admin of this chapter can create publication only for their chapter
            instance.chapters = request.user.chapter
        elif self.request.user.user_type == 'super_admin':
            # Super admin creates national publication (no specific chapter)
            instance.chapters = None  # Chapters are None for national
        exco = None
        exco_id = request.data.get('exco_id', None)
        if exco_id:
            # If exco_id is provided, associate this publication with the specified ExcoRole
            exco = get_object_or_404(user_related_models.ExcoRole, id=exco_id)
        instance.exco = exco
        instance.save()
        clean_data = self.serializer_class(instance, many=False)
        return custom_response.Success_response(msg='Publication created successfully', data=[clean_data.data], status_code=status.HTTP_201_CREATED)

    # def list(self, request, *args, **kwargs):
    #     queryset = models.Publication.objects.all()
    #     clean_data = self.serializer_class(queryset, many=True)
    #     return custom_response.Success_response(msg='Success', data=clean_data.data, status_code=status.HTTP_200_OK)
    
    def list(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return custom_response.Success_response(msg='Authentication required', data=[], status_code=status.HTTP_401_UNAUTHORIZED)
        
        # Get all publications
        queryset = models.Publication.objects.all()
        
        # Filter publications for logged-in users based on the 'is_for_members_only' flag
        if not request.user.is_authenticated:
            queryset = queryset.filter(is_for_members_only=False)
        
        # If the user is logged in, include the publications with is_for_members_only=True
        else:
            # Optionally, filter publications based on the user's chapter or role if needed
            if request.user.user_type == 'admin':
                queryset = queryset.filter(chapters=request.user.chapter)
            elif request.user.user_type == 'super_admin':
                queryset = queryset.all()  # No chapter filter for super_admin
            
            # You can also add additional filters based on user attributes or roles
        
        clean_data = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg='Success', data=clean_data.data, status_code=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        'Partially update a Publication'
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True, context={"request": request})
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()
        
        if self.request.user.user_type == 'admin' and 'chapters' in request.data:
            updated_instance.chapters = request.user.chapter
        elif self.request.user.user_type == 'super_admin' and 'chapters' in request.data:
            updated_instance.chapters = None
        
        exco_id = request.data.get('exco_id', None)
        if exco_id:
            exco = get_object_or_404(user_related_models.ExcoRole, id=exco_id)
            updated_instance.exco = exco
        
        updated_instance.save()
        clean_data = self.serializer_class(updated_instance, many=False)
        return custom_response.Success_response(msg='Publication updated successfully', data=[clean_data.data], status_code=status.HTTP_200_OK)



# class AdminManagePublication(viewsets.ModelViewSet):
#     queryset = models.Publication.objects.all()
#     permission_classes = [permissions.IsAuthenticated,custom_permission.IsAdminOrSuperAdmin,custom_permission.Normal_Admin_Must_BelongToACHapter]
#     serializer_class = serializers.AdminManagePublicationSerializer
#     parser_classes =(custom_parsers.NestedMultipartParser,FormParser,)

#     def create(self,request,format=None):
#         'create Publication'
#         serialize =  self.serializer_class(data=request.data,context={"request":request})
#         serialize.is_valid(raise_exception=True)
#         instance = serialize.save()
#         if self.request.user.user_type in ['admin']:
#             # this means this is a admin of this chapter we force him to create the news only for his chapter
#             instance.chapters = request.user.chapter
#         if self.request.user.user_type in ['super_admin']:
#             # this means this person is a super_amin this means this news would be National
#             instance.chapters= None#chapters are none for national
#         exco =None
#         exco_id = request.data.get('exco_id',None)
#         if exco_id:
#             "this means the user want to make this event for this type of exco"
#             try:
#                 exco =get_object_or_404(user_related_models.ExcoRole,id=exco_id)
#             except:
#                 raise CustomError({'error':'Exco Does not exist'})
#         instance.exco=exco
#         instance.save()
#         # duesObject = models.Event.objects.all().filter(id=instance.id).values()
#         clean_data = self.serializer_class(instance,many=False)
#         return custom_response.Success_response(msg='Publication created successfully',data=[clean_data.data],status_code=status.HTTP_201_CREATED) 

#     def list(self, request, *args, **kwargs):
#         queryset = models.Publication.objects.all()
#         clean_data = self.serializer_class(queryset,many=True)
#         return custom_response.Success_response(msg='Success',data=clean_data.data,status_code=status.HTTP_200_OK) 

#     def destroy(self, request, *args, **kwargs):
#         return super().destroy(request, *args, **kwargs)



class GetUnauthorizedPublications(views.APIView):
    permission_classes =[permissions.AllowAny]
    
    # def _return_newsInDIct(self,publication):
    #     return {"name":publication.name,}

    # def get(self, request):
    #     "this wil get the publication based on the news specs"

    #     all_publication=models.Publication.objects.all().order_by('-created_at')
    #     filter_set = custom_filter.PublicationLookUp(request.query_params,queryset=all_publication)
    #     serialized = serializers.AdminManagePublicationSerializer(filter_set.qs,many=True,context={"request":request})
    #     return custom_response.Success_response(msg='success',data=serialized.data,status_code=status.HTTP_200_OK)

    def get(self, request):
        """
        This will get the publications based on the news specs.
        Filters out publications based on the `is_for_members_only` field and user's authentication status.
        """

        # Fetch all publications
        all_publication = models.Publication.objects.all().order_by('-created_at')

        # Apply the `is_for_members_only` filter
        if not request.user.is_authenticated:
            all_publication = all_publication.filter(is_for_members_only=False)

        # Apply additional query parameter-based filtering
        filter_set = custom_filter.PublicationLookUp(request.query_params, queryset=all_publication)

        # Serialize the filtered queryset
        serialized = serializers.AdminManagePublicationSerializer(
            filter_set.qs, many=True, context={"request": request}
        )

        # Return the response
        return custom_response.Success_response(
            msg='success',
            data=serialized.data,
            status_code=status.HTTP_200_OK
        )



class GetUnAuthorizedPublication(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, pk): 
        publication_instance = get_object_or_404(models.Publication,id=pk)
        serializer = serializers.AdminManagePublicationSerializer(publication_instance,many=False)
        return custom_response.Success_response(msg="Success",data=serializer.data,status_code=status.HTTP_200_OK)


class MembersGetPublications(views.APIView):
    # serializer_class  = 
    permission_classes =[permissions.IsAuthenticated,custom_permission.IsMember,custom_permission.Isfinancial]
    
    def _return_newsInDIct(self,publication):return {"name":publication.name,}


    def get(self, request, format=None):
        "this wil get the publication based on the news specs"

        all_publication=models.Publication.objects.all().order_by('-created_at')
        filter_set = custom_filter.PublicationLookUp(request.query_params,queryset=all_publication)
        serialized = serializers.AdminManagePublicationSerializer(filter_set.qs,many=True,context={"request":request})
        return custom_response.Success_response(msg='success',data=serialized.data,status_code=status.HTTP_200_OK)


    def post(self, request, format=None): 
        likes = request.data.get('like')
        dislikes= request.data.get('dislike')
        id =request.data.get('id',None)
        
        if id:
            if models.Publication.objects.filter(id=id).exists():
                news = models.Publication.objects.get(id=id)
                
                if likes == True:
                    if news.likes  is None:news.likes =1
                    else:news.likes += 1
                if dislikes  == True:
                    if  news.dislikes is None: news.dislikes =1
                    else:news.dislikes +=1
                news.save()
                return custom_response.Success_response(msg='Publications was updated  successfully',data=[{
                    "likes": news.likes,
                    "dislikes":news.dislikes,
                    "id":news.id
                }],status_code=status.HTTP_201_CREATED)

        raise CustomError({"error":"News Doesnt exist's"})


class MemberCommentOnPublication(viewsets.ModelViewSet):
    queryset = models.PublicationComment.objects.all()
    permission_classes =[permissions.IsAuthenticated,custom_permission.IsMember]
    serializer_class = serializers.MemberCommentOnPublicationSerializer

    
    def perform_create(self, serializer):
        serializer.save(member=self.request.user.memeber)

    def list(self, request, *args, **kwargs):
        publication_id = self.request.query_params.get('publication_id',None)
        publication = get_object_or_404(models.Publication,id=publication_id)
        data = self.queryset.filter(news=publication)
        clean_data = self.serializer_class(instance=data,many=True)

        return custom_response.Success_response('Success',data=clean_data.data,)