from rest_framework import viewsets
from utils import permissions as custom_permission
from rest_framework import permissions,status
from . import models,serializers
from utils import custom_response


class ManageMinute(viewsets.ModelViewSet):
    queryset = models.Minute.objects.all()
    serializer_class = serializers.MinuteSerializers
    permission_classes = [permissions.IsAuthenticated,custom_permission.IsMember,custom_permission.IsExco,custom_permission.CanUploadMin]

    def create(self, request, *args, **kwargs):
        serialzed = self.serializer_class(data=request.data)
        serialzed.is_valid(raise_exception=True)
        serialzed.save()

        
        minute = models.Minute.objects.get(id= serialzed.data.get('id'))
        minute.chapter = request.user.chapter

        minute.save()
        file_url =None
        if minute.file:
            file_url = minute.file.url
        return custom_response.Success_response(msg="created",data=[{
            "id":minute.id,
            "file":file_url,
            "name":minute.name,
            'chapter':minute.chapter.id
            # 'chapter_name':minute.chapter.id

        }],status_code=status.HTTP_201_CREATED)

class ViewMinute(viewsets.ViewSet):
    queryset = models.Minute.objects.all()
    # serializer_class = serializers.MinuteSerializers
    permission_classes = [permissions.IsAuthenticated,custom_permission.IsExco]

    def list(self, request, *args, **kwargs):
        is_chapter = self.request.query_params.get('is_chapter',None)
        all_min = self.queryset
        if is_chapter:all_events=all_min.filter(chapter = request.user.chapter)
        else:all_events=all_min.filter(chapter =None)
        return custom_response.Success_response(msg='success',data=all_min.values(),status_code=status.HTTP_200_OK)

