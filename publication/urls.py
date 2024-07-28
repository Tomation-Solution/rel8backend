from django.urls import path
from rest_framework.routers import  DefaultRouter
from . import models
from . import views





router = DefaultRouter()
router.register("publicationview",views.AdminManagePublication,basename='publication')
router.register('publicationview__comment',views.MemberCommentOnPublication)


urlpatterns = [
    path('getyourpublication/',views.MembersGetPublications.as_view(),name='getyourpublication').
    path('unauthorized_publications/',views.GetUnauthorizedPublications.as_view(),name='unauthorized_publications')
] +router.urls
