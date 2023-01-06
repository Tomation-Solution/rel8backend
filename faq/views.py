from rest_framework import viewsets,permissions
from rest_framework.decorators import action
from utils import permissions as custom_permissions
from .  import models,serializers
from utils import custom_response







class ManageFaq(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,custom_permissions.IsSuperAdmin]
    queryset =  models.FAQ.objects.all()
    serializer_class = serializers.ManageFaqSerializer



    @action(detail=False,methods=['get'],permission_classes = [])
    def members_view_faq(self,request,format=None):
        "members see faq"
        return custom_response.Success_response(msg='success',data=models.FAQ.objects.all().values())
