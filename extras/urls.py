from django.urls import path
from rest_framework.routers import  DefaultRouter
from . import models
from . import views





router = DefaultRouter()
router.register("galleryview",views.GalleryView,basename='gallery')
router.register("ticketview",views.TicketingView,basename='ticketing')
router.register('gallery_version2',views.GalleryV2View,basename='gallery_version2')
router.register('admin_gallery_version2',views.AdminManageGalleryV2View,basename='admin_gallery_version2')
router.register('admin_manage_project',views.AdminManagesProjectViewset)
router.register('member_support_project_kind',views.MemeberProjectSupportKindViewset,basename='member_support_project_kind')
router.register('member_support_project_cash',views.MemeberProjectSupportCashViewset,basename='member_support_project_cash')
router.register('memeber_customer_support',views.MemeberCustomerSupportViewSet)
router.register('member_personal_gallery',views.MemberPersonalGallery,basename='member_personal_gallery')
urlpatterns =[
    path('project/payment/', views.FundAProjectPayment.as_view(), name="fund_project_payment"),
    path('gallery_version2/unauthorized_images/<int:pk>/', views.GetUnAuthorizedGalleryFolder.as_view(), name="get_gallery_folder"),
    path('admin_gallery_version2/delete_images/', views.AdminGalleryV2ImagesDeletionView.as_view(), name="admin_gallery_v2_images_deletion"),
    path('projects/cash/support', views.AdminProjectSupportByCashView.as_view(), name="project_cash_support"),
    path('projects/kind/support', views.AdminProjectSupportInKindView.as_view(), name="project_kind_support"),
] + router.urls