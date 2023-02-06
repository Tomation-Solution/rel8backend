from django.urls import path
from rest_framework.routers import  DefaultRouter
from . import models
from . import views





router = DefaultRouter()
router.register("publicationview",views.AdminManagePublication,basename='publication')
router.register('publicationview__comment',views.MemberCommentOnPublication)


urlpatterns = [
    path('getyourpublication/',views.MembersGetNews.as_view(),name='getyourpublication')
] +router.urls
