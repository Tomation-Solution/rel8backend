from django.urls import path
from rest_framework.routers import  DefaultRouter
from . import models
from . import views




router = DefaultRouter()
router.register("faq",views.ManageFaq,basename='faq')


urlpatterns = [
] +router.urls
