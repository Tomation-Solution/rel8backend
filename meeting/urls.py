from rest_framework.routers import  DefaultRouter
from .views import MeetingMemberViewSet,AdminManagesMeetingViewset






router = DefaultRouter()

router.register('meeting_member',MeetingMemberViewSet,basename='meeting_member')
router.register('admin_manage_meeting',AdminManagesMeetingViewset)

urlpatterns = [
   
] +router.urls
