from django.urls import path
from rest_framework.routers import  DefaultRouter
from . import models
from . import views





router = DefaultRouter()
router.register("newsview",views.AdminManageNews,basename='news')
router.register('newsview__comment',views.MemberCommentOnNews)

urlpatterns = [
    path('getyournews/',views.MembersGetNews.as_view(),name='getyournews'),
    path('unauthorized_news/', views.GetAllUnAuthorizedNews.as_view(), name="unauthorized_news"),
    path('unauthorized_news/<int:pk>/', views.GetUnAuthorizedNews.as_view(), name="unauthorized_news")
] +router.urls
