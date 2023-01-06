from rest_framework.pagination import PageNumberPagination
from . import custom_response 
from . import extraFunc
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import status
from math import ceil

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 200



class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50
    page_query_param = "page"

    def get_paginated_response(self,data):
        # this is where i write my custom  pagination

        
        # data = custom_response.structure_responseDict(msg="All data",status_code= 200,success=True,data=data)
        total_data_count =self.page.paginator.count
        page_count = ceil(total_data_count/ self.page_size)
        numOfPages = self.cal_page_numbers(total_data_count)
        
        # paginated_data= self.serializer_class(data,many=True,context={'request':request})

        def makeData(num):return {
            'url':self.build_url(num),
            'label':num,
            'active':self.get_active(num,)
        }

        list_of_links=map(makeData,numOfPages)
        return {
            'links':list_of_links,
            'current_page':self.request.query_params.get('page',1),
            'data':data,
            'last_page_url':len(numOfPages),
            'first_page_url':numOfPages[0],
            'pages_number':page_count,
        }
    def get_active(self,num):
        return int(self.request.query_params.get('page',1))==num


    def build_url(self,page_number):
        url = self.request.build_absolute_uri()
        return extraFunc.replace_query_param(url,self.page_query_param,page_number)

    def cal_page_numbers(self,total_items):
        num_of_pages = ceil(total_items/self.page_size)
        if(num_of_pages==0):return [1]

        return [num+1 for num in range(num_of_pages)]





class PageNumPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50
    page_query_param = "page"

    def get_paginated_response(self, data):
        
        data = custom_response.structure_responseDict(msg="All data",status_code= 200,success=True,data=data)
        data["count"] = self.page.paginator.count
        data["next"] = self.get_next_link()
        data["previous"] = self.get_previous_link()
        data["page_count"] = ceil(data["count"] / self.max_page_size)
        return Response(data, status=status.HTTP_200_OK)
