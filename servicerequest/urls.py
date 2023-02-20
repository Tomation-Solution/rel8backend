
from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


route = DefaultRouter()

route.register('reissuance_of_certificate',views.MemberOfReissuanceOfCertificateViewset)
route.register('Change_of_name',views.ChangeOfNameViewset)
route.register('merger_of_companies',views.MergerOfCompaniesViewset)
route.register('deactivation_of_membership',views.DeactivationOfMembershipViewset)
route.register('product_manufacturing_update',views.ProductManufacturingUpdateViewset)
route.register('factoryLocation_update',views.FactoryLocationUpdateViewset)

urlpatterns  =[ 
] + route.urls