from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


route = DefaultRouter()

route.register('payment-notification',views.PaymentNotification,basename='payment-notification')
route.register('',views.PaymentValidation,basename='payment_validation')

urlpatterns = [ 
    # path('',)
] + route.urls