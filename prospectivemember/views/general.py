from rest_framework import viewsets
from utils.custom_response import Success_response
from rest_framework import status
from prospectivemember import general_serializer

class CreatePropectiveMemberViewset(viewsets.ViewSet):
    serializer_class = general_serializer.CreatePropectiveMemberSerializer

    def create(self,request,*args,**kwargs):
        serialized= self.serializer_class(data=request.data,context={'request':request})
        serialized.is_valid(raise_exception=True)
        response_info = serialized.save()

        return Success_response('Creation Success',data=[],status_code=status.HTTP_201_CREATED)
