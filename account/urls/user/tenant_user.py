from django.contrib import admin
from django.urls import path,include
from ...views  import user as user_view
from rest_framework.routers import  DefaultRouter


router = DefaultRouter()
router.register("ManageAssigningExcos",user_view.ManageAssigningExcos,basename='ManageAssigningExcos')
router.register("CreateAnyAdminType",user_view.CreateAnyAdminType,basename='CreateAnyAdminType')
router.register("RegisterUserToChapter",user_view.RegisterUserToChapter,basename='RegisterUserToChapter')
router.register("AdminRelatedViews",user_view.AdminRelatedViews,basename='AdminRelatedViews')
router.register('memberlist-info',user_view.MemberListInfo,basename="memberlist-info")
router.register('member-bio',user_view.MemberBioViewSet,basename='member-bio')
router.register('update-member-info',user_view.UpdateMemberInfoViewSet,basename='update-member-info')
router.register('forgot-password',user_view.ForgotPasswordViewSet,basename='forgot-password')


urlpatterns = [
    path('profile/',user_view.profile,name='profile'),
    path('council_members/<int:pk>/',user_view.council_members,name='council_members'),
    path('get_membershipgrade/',user_view.get_membershipgrade,name='get_membershipgrade'),
    path('chapters', user_view.GetExistingChapters.as_view(), name="get_existing_chapters"),
    path('exco_roles', user_view.ListExcoRolesView.as_view(), name='get_exco_roles'),
    path('exco_roles/remove_member', user_view.RemoveMemberFromExcoRoleView.as_view(), name="remove_member")
] +router.urls
