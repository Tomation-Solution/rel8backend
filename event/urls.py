from rest_framework.routers import  DefaultRouter
from Dueapp.views import payments as payment_views
from . import views





router = DefaultRouter()
router.register("eventview",views.EventViewSet,basename='eventview')
router.register('request-reschedule',views.RescheduleEventRequestViewSet,basename='request-reschedule')
urlpatterns = [
   
] +router.urls
