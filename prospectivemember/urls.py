from rest_framework.routers import  DefaultRouter
from prospectivemember.views import man as man_views
from prospectivemember.views import general as general_view
router = DefaultRouter()
# below are endpoint for only MAN
router.register('creation_of_prospective_member',man_views.CreateManPropectiveMemberViewset,basename='creation_of_prospective_member')
router.register('propective_member_manage_form_one',man_views.PropectiveMemberManageFormOneViewSet,basename='propective_member_manage_form_one')
router.register('propective_member_manage_form_two',man_views.PropectiveMemberManageFormTwo,basename='propective_member_manage_form_one')

# BELOW ARE view set for all the rest of the tenenat
router.register('create_propective_member',general_view.CreatePropectiveMemberViewset,basename='create_propective_member')
router.register('general_propective_member_manage_form_one',general_view.PropectiveMemberHandlesFormOneViewSet,basename='general_propective_member_manage_form_one')
router.register('general_propective_member_manage_form_two',general_view.PropectiveMemberHandlesFormTwoViewSet,basename='general_propective_member_manage_form_two')
router.register('update_uploadedfiles_formtwo',general_view.UpdateFomrTwoViewSet,basename='update_uploadedfiles_formtwo')
router.register('adminManage_prospective_rule',general_view.AdminManageProspectiveRuleViewSet,basename='adminManage_prospective_rule')
urlpatterns = [
   
] +router.urls
