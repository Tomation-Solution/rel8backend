from django.urls import path
from rest_framework.routers import  DefaultRouter
from . import views



router = DefaultRouter()
router.register("adminmanageballotbox",views.AdminManageBallotBox,basename='adminmanageballotbox')


urlpatterns =[
    # path('')
]+ router.urls