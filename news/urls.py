from django.urls import path
from rest_framework.routers import  DefaultRouter
from . import models
from . import views





router = DefaultRouter()
router.register("newsview",views.AdminManageNews,basename='news')


urlpatterns = [
    path('getyournews/',views.MembersGetNews.as_view(),name='getyournews')
] +router.urls
