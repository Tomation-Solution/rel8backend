from rest_framework.routers import  DefaultRouter
from prospectivemember.views import man as man_views

router = DefaultRouter()
router.register('creation_of_prospective_member',man_views.CreateManPropectiveMemberViewset,basename='creation_of_prospective_member')
router.register('propective_member_manage_form_one',man_views.PropectiveMemberManageFormOneViewSet,basename='propective_member_manage_form_one')
router.register('propective_member_manage_form_two',man_views.PropectiveMemberManageFormTwo,basename='propective_member_manage_form_one')

urlpatterns = [
   
] +router.urls
