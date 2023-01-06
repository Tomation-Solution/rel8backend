
from rest_framework.routers import  DefaultRouter
from . import views

router = DefaultRouter()


router.register("manageminute",views.ManageMinute,basename='manageminute')
router.register("excos_view_minutes",views.ViewMinute,basename='manageminute')

urlpatterns = [
   
] +router.urls
