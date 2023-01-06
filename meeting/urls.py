from rest_framework.routers import  DefaultRouter
from .views import MeetingMemberViewSet






router = DefaultRouter()

router.register('meeting_member',MeetingMemberViewSet,basename='meeting_member')


urlpatterns = [
   
] +router.urls
