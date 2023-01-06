from rest_framework.routers import  DefaultRouter
from django.contrib import admin
from django.urls import path
from . import views

router = DefaultRouter()
router.register("subscription",views.SubscriptionViewSet,basename='subscription')



urlpatterns  =[

] +router.urls