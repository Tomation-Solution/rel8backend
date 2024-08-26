from rest_framework.routers import  DefaultRouter
from Dueapp.views import payments as payment_views
from . import views
from django.urls import path




router = DefaultRouter()
router.register("eventview",views.EventViewSet,basename='eventview')
router.register('request-reschedule',views.RescheduleEventRequestViewSet,basename='request-reschedule')
urlpatterns = [
    path('unauthorized_events/', views.UnauthorizedEventView.as_view(), name="unauthorized_events"),
    path('unauthorized_events/<int:pk>/', views.UnauthorizedEventView.as_view(), name="unauthorized_events"),
    path('/payment/', views.EventPaymentView.as_view(), name="event_payment")
] +router.urls
