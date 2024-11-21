from rest_framework.routers import  DefaultRouter
from django.urls import path
from . import views



router = DefaultRouter()


router.register('admin_manage_reminder',views.AdminManageReminderViewSet, basename="admin_reminder")
router.register('member_reminder',views.MembersReminderViewSet, basename="member_reminder_view")


urlpatterns = [] +router.urls
