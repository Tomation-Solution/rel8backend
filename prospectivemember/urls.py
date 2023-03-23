from rest_framework.routers import  DefaultRouter
from prospectivemember.views import man as man_views

router = DefaultRouter()
router.register('creation_of_prospective_member',man_views.CreateManPropectiveMemberViewset,basename='creation_of_prospective_member')

urlpatterns = [
   
] +router.urls
