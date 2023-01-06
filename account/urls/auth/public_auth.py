from django.contrib import admin
from django.urls import path,include
from ...views  import auth as auth_view
from ...views  import user as user_view
urlpatterns = [
    path('create_superadmin/',auth_view.RegisterSuperAdmin.as_view()),
    path('create_alumn/',user_view.CreateAlumni.as_view(),name='create-alumni'),
    path('login/',auth_view.Login.as_view(),),

]
