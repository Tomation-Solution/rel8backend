from django.contrib import admin
from django.urls import path,include
from .views import detail as detail_views
from .views import payments as payments_views
from rest_framework.routers import  DefaultRouter


router = DefaultRouter()
router.register("AdminManageDue",detail_views.AdminManageDue,basename='AdminManageDue')
router.register("AdminManageDeactivatingDue",detail_views.AdminManageDeactivatingDue,basename='AdminManageDeactivatingDue')
router.register("memberdue",detail_views.MemberDues,basename='MemberDues')


# AdminManageDeactivatingDuesSerializer


urlpatterns = [
    path('process_payment/<str:forWhat>/<int:pk>/',payments_views.InitPaymentTran.as_view(),name='process_payment'),
    # path('webhook/',payments_views.useWebhook)
] +router.urls
