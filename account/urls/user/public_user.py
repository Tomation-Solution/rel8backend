from django.contrib import admin
from django.urls import path,include
from ...views  import user as user_view

urlpatterns = [
    path('create_alumni/',user_view.CreateAlumni.as_view()),
]
