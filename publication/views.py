from django.shortcuts import render
from rest_framework import viewsets,permissions,views,status

from utils.custom_exceptions import CustomError
from . import models
from utils import permissions as custom_permission
from . import serializers,filter as custom_filter
from account.models import user as user_related_models
from utils import custom_response,custom_parsers
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


class AdminManagePublication(viewsets.ModelViewSet):
    queryset = models.Publication.objects.all()
    permission_classes = [permissions.IsAuthenticated,custom_permission.IsAdminOrSuperAdmin,custom_permission.Normal_Admin_Must_BelongToACHapter]
    serializer_class = serializers.AdminManagePublicationSerializer
    parser_classes =(custom_parsers.NestedMultipartParser,FormParser,)

    def create(self,request,format=None):
        'create Publication'
        serialize =  self.serializer_class(data=request.data,context={"request":request})
        serialize.is_valid(raise_exception=True)
        instance = serialize.save()
        if self.request.user.user_type in ['admin']:
            # this means this is a admin of this chapter we force him to create the news only for his chapter
            instance.chapters = request.user.chapter
        if self.request.user.user_type in ['super_admin']:
            # this means this person is a super_amin this means this news would be National
            instance.chapters= None#chapters are none for national
        exco =None
        exco_id = request.data.get('exco_id',None)
        if exco_id:
            "this means the user want to make this event for this type of exco"
            try:
                exco =get_object_or_404(user_related_models.ExcoRole,id=exco_id)
            except:
                raise CustomError({'error':'Exco Does not exist'})
        instance.exco=exco
        instance.save()
        # duesObject = models.Event.objects.all().filter(id=instance.id).values()
        clean_data = self.serializer_class(instance,many=False)
        return custom_response.Success_response(msg='Publication created successfully',data=[clean_data.data],status_code=status.HTTP_201_CREATED) 

    def list(self, request, *args, **kwargs):
        queryset = models.Publication.objects.all()
        clean_data = self.serializer_class(queryset,many=True)
        return custom_response.Success_response(msg='Success',data=clean_data.data,status_code=status.HTTP_200_OK) 

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
class MembersGetNews(views.APIView):
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