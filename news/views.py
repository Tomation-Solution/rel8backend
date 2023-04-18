from django.shortcuts import render
from rest_framework import viewsets,permissions,views,status
from utils.custom_exceptions import CustomError
from . import models
from utils import permissions as custom_permission
from . import serializers,filter as custom_filter
from account.models import user as user_models
from utils import custom_response,custom_parsers
from account.models import user as user_related_models
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


class AdminManageNews(viewsets.ModelViewSet):
    queryset = models.News.objects.all()
    permission_classes = [permissions.IsAuthenticated,custom_permission.IsAdminOrSuperAdmin,custom_permission.Normal_Admin_Must_BelongToACHapter]
    serializer_class = serializers.AdminManageNewSerializer
    parser_classes =(custom_parsers.NestedMultipartParser,FormParser,)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    def create(self,request,format=None):
        'create event'
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
        clean_data =self.serializer_class(instance,many=False, context={'request': request},)
        return custom_response.Success_response(msg='News created successfully',data=[clean_data.data,],status_code=status.HTTP_201_CREATED)
    def list(self, request, *args, **kwargs):
        'this code let chapter see thier news '
        all_news = models.News.objects.all()
        if self.request.query_params.get('is_chapter',None):all_news=all_news.filter(chapters = request.user.chapter)
        else:all_news=all_news.filter(chapters =None)
        serialized = self.serializer_class(all_news,many=True, context={'request': request},)

        return custom_response.Success_response(msg='success',data=serialized.data,status_code=status.HTTP_200_OK)

    @action(detail=False,methods=['get'],permission_classes = [permissions.IsAuthenticated,custom_permission.IsMember])
    def get_news(self,request,format=None):

        all_news=models.News.objects.all().order_by('-created_at')
        filter_set  = custom_filter.NewsLookUp(request.query_params,queryset=all_news)
        clean_data = self.serializer_class(filter_set.qs,many=True,context={'request':self.request})
        return custom_response.Success_response(msg='success',data=clean_data.data,status_code=status.HTTP_200_OK)

class MembersGetNews(views.APIView):
    # serializer_class  = 
    permission_classes =[permissions.IsAuthenticated,custom_permission.IsMember]

    def _return_newsInDIct(self,news):
        # print({
        #      "hasReacted":news.user_that_have_reacted.all().filter(id=self.request.user.memeber.id).exists()
        # })
        image = None
        if news.image:
            image =  self.request.build_absolute_uri(news.image.url)#https://stackoverflow.com/questions/35522768/django-serializer-imagefield-to-get-full-url/48142428#48142428
        return {"id":news.id,"name":news.name,'likes':news.likes,
    'dislikes':news.dislikes,'is_member':news.is_member,
    'is_committe':news.is_committe,"is_exco":news.is_exco,
    "hasReacted":news.user_that_have_reacted.all().filter(id=self.request.user.memeber.id).exists(),
    "image":image
    }



    def post(self, request, format=None): 
        likes = request.data.get('like')
        dislikes= request.data.get('dislike')
        id =request.data.get('id',None)
        
        if id:
            if models.News.objects.filter(id=id).exists():
                news = models.News.objects.get(id=id)
                # print({
                #     "user":request.user.memeber,
                #     "members that have liked":news.user_that_have_reacted.all().filter(id=request.user.memeber.id)
                # })
                if not news.user_that_have_reacted.all().filter(id=request.user.memeber.id).exists():
                    news.user_that_have_reacted.add(request.user.memeber)
                    if likes == True:
                        if news.likes  is None:news.likes =1
                        else:news.likes += 1
                    if dislikes  == True:
                        if  news.dislikes is None: news.dislikes =1
                        else:news.dislikes +=1
                else:
                    print("You have DOn this alreayd")
                        
                news.save()
                return custom_response.Success_response(msg='News was updated  successfully',data=[{
                    "likes": news.likes,
                    "dislikes":news.dislikes,
                    "id":news.id
                }],status_code=status.HTTP_201_CREATED)

        raise CustomError({"error":"News Doesnt exist's"})


class MemberCommentOnNews(viewsets.ModelViewSet):
    queryset = models.NewsComment.objects.all()
    permission_classes =[permissions.IsAuthenticated,custom_permission.IsMember,custom_permission.Isfinancial]
    serializer_class = serializers.MemberCommentOnNewsSerializer

    
    def perform_create(self, serializer):
        serializer.save(member=self.request.user.memeber)

    def list(self, request, *args, **kwargs):
        news_id = self.request.query_params.get('news_id',None)
        news = get_object_or_404(models.News,id=news_id)
        data = self.queryset.filter(news=news)
        clean_data = self.serializer_class(instance=data,many=True)

        return custom_response.Success_response('Success',data=clean_data.data,)