from django.contrib import admin
from django.urls import path,include
from ...views  import auth as auth_view
from rest_framework.routers import  DefaultRouter


router = DefaultRouter()

router.register('ManageMemberValidation',auth_view.ManageMemberValidation,basename='ManageMemberValidation')
router.register("manage-commitee-member",auth_view.AdminManageCommiteeGroupViewSet,basename="manage-commitee-member")
router.register('manage-chapter',auth_view.SuperAdminMangeChapters,basename='manage-chapter')
router.register('manage-commitee-member-postions',auth_view.AdminManageCommiteeGroupPostionsViewSet,basename='manage-commitee-member-postions')
urlpatterns = [

    path('login/',auth_view.Login.as_view(),),
    path('upload_database/',auth_view.UploadSecondLevelDataBaseView.as_view(),name='upload_database'),
    path( "validate-email/",auth_view.EmailValidateView.as_view(),name="email-validate"),
    path('pusher/beams-auth/',auth_view.beams_auth),
    path('send/',auth_view.send_data),
    path('member/commitees',auth_view.MemberCommiteeView.as_view(), name='get_commitees_for_members'),
    path('manage-committee-members/{committee_id}/members/{member_id}/',
        auth_view.DeleteCommitteeMemberView.as_view(),
        name="delete_committee_members"
    )

]+ router.urls

