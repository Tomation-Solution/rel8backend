from django.contrib import admin
from django.urls import path,include
from ...views  import user as user_view
from rest_framework.routers import  DefaultRouter


router = DefaultRouter()
router.register("ManageAssigningExos",user_view.ManageAssigningExos,basename='ManageAssigningExos')
router.register("CreateAnyAdminType",user_view.CreateAnyAdminType,basename='CreateAnyAdminType')
router.register("RegisterUserToChapter",user_view.RegisterUserToChapter,basename='RegisterUserToChapter')
router.register("AdminRelatedViews",user_view.AdminRelatedViews,basename='AdminRelatedViews')
router.register('memberlist-info',user_view.MemberListInfo,basename="memberlist-info")
router.register('member-bio',user_view.MemberBioViewSet,basename='member-bio')
urlpatterns = [
    path('profile/',user_view.profile,name='profile'),
    path('council_members/<int:pk>/',user_view.council_members,name='council_members'),
    path('get_membershipgrade/',user_view.get_membershipgrade,name='get_membershipgrade')
] +router.urls
