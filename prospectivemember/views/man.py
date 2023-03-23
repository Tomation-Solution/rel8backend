from prospectivemember.models import man_prospective_model as manrelatedPropectiveModels
from prospectivemember import serializer
from rest_framework import viewsets
from utils.custom_response import Success_response
from rest_framework import status



class CreateManPropectiveMemberViewset(viewsets.ViewSet):

    serializer_class = serializer.CreateManPropectiveMemberSerializer

    def create(self,request,*args,**kwargs):
        serialized= self.serializer_class(data=request.data,)
        serialized.is_valid(raise_exception=True)
        serialized.save()

        return Success_response('Creation Success',data=[],status_code=status.HTTP_201_CREATED)