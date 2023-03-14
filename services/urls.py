
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import  members as members_views
from .views import admin as admin_views
route = DefaultRouter()
route.register('Change_of_name',members_views.ChangeOfNameViewset)
route.register('loss_of_certificate',members_views.MemberLossOfCertificateServiceViewSet)
route.register('deactivation_of_membership',members_views.DeactivationOfMembershipViewset)
route.register('product_manufacturing_update',members_views.ProductManufacturingUpdateViewset)
route.register('activation_of_deactivated_member',members_views.ActivationOfDeactivatedMemberViewSet)
route.register('reissuance_of_cert_services',members_views.ReissuanceOfCertServicesViewSet)
# route.register('merger_of_companies',views.MergerOfCompaniesViewset)
# route.register('factory_location_update',views.FactoryLocationUpdateViewset)

route.register('admin_manage_change_of_name',admin_views.AdminManageChangeOfNameView)
route.register('admin_loss_of_certificate_service',admin_views.AdminLossOfCertificateServiceViewSet)
route.register('admin_deactivation_of_membership',admin_views.AdminDeactivationOfMembershipViewset)
route.register('admin_product_manufacturing_update',admin_views.AdminProductManufacturingUpdateViewset)
route.register('admin_activation_of_deactivated_member',admin_views.AdminActivationOfDeactivatedMemberViewSet)
urlpatterns = [

]+route.urls