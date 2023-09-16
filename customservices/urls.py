from rest_framework.routers import DefaultRouter
from .  import views

route = DefaultRouter()

route.register('rel8-custom-services',views.AdminRel8CustomServicesViewset)
route.register('rel8-custom-services-member-handler',views.MembersRel8CustomerServiceViewset,basename='rel8-custom-services-member-handler')


urlpatterns =[

]+route.urls