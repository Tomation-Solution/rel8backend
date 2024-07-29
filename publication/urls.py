from django.urls import path
from rest_framework.routers import  DefaultRouter
from . import models
from . import views





router = DefaultRouter()
router.register("publicationview",views.AdminManagePublication,basename='publication')
router.register('publicationview__comment',views.MemberCommentOnPublication)


urlpatterns = [
    path('getyourpublication/',views.MembersGetPublications.as_view(),name='getyourpublication'),
    path('unauthorized_publications/',views.GetUnauthorizedPublications.as_view(),name='unauthorized_publications'),
    path('unauthorized_publications/<int:pk>/', views.GetUnAuthorizedPublication.as_view(), name="get_gallery_folder"),
] +router.urls
