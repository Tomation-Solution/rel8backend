from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
route = DefaultRouter()

route.register('admin_lastest_updates',views.AdminLastestUpdatesViewSet, basename="admin_latest_updates")
route.register('member_lastest_updates',views.MemberLastestUpdatesViewSet, basename="member_lastest_updates")


urlpatterns = [
]+route.urls