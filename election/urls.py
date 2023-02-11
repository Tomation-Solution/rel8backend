from django.urls import path
from rest_framework.routers import  DefaultRouter
from . import views



router = DefaultRouter()
router.register("adminmanageballotbox",views.AdminManageBallotBox,basename='adminmanageballotbox')
router.register('postion_manager',views.PostionViewset)

urlpatterns =[
    # path('')
]+ router.urls