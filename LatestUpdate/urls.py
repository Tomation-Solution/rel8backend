from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
route = DefaultRouter()

route.register('admin_lastest_updates',views.AdminLastestUpdatesViewSet)
route.register('member_lastest_updates',views.MemberLastestUpdatesViewSet)


urlpatterns = [
]+route.urls