from django.urls import path
from rest_framework.routers import  DefaultRouter
from . import models
from . import views





router = DefaultRouter()
router.register("galleryview",views.GalleryView,basename='gallery')
router.register("ticketview",views.TicketingView,basename='ticketing')
router.register('gallery_version2',views.GalleryV2View,basename='gallery_version2')
router.register('admin_gallery_version2',views.AdminManageGalleryV2View,basename='admin_gallery_version2')
router.register('admin_manage_project',views.AdminManagesProjectViewset,)
router.register('member_support_project',views.MemeberProjectViewset,basename='member_support_project')
router.register('memeber_customer_support',views.MemeberCustomerSupportViewSet)
urlpatterns =[

] + router.urls