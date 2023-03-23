"""rel8 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('tenant/auth/',include('account.urls.auth.tenant_auth')),
    path('tenant/user/',include('account.urls.user.tenant_user')),
    path('tenant/dues/',include('Dueapp.urls')),
    path('tenant/event/',include("event.urls")),
    path('tenant/news/',include("news.urls")),
    path('tenant/publication/',include("publication.urls")),
    path('tenant/extras/',include('extras.urls')),
    path('tenant/election/',include('election.urls')),
    path('tenant/subscribe/',include('subscription.urls')),
    path("tenant/minute/",include('minute.urls')),
    path("tenant/faq/",include('faq.urls')),
    path("tenant/reminder/",include('reminders.urls')),
    path("tenant/chat/",include('chat.urls')),
    path("tenant/meeting/",include('meeting.urls')),
    path('tenant/services_request/',include('services.urls')),
    path('tenant/latestupdate/',include('LatestUpdate.urls')),

    path('tenant/mailing/',include('mailing.urls')),
    path('interswitch_payment/',include('interswitchapp.urls')),
    path('mailing/',include('mymailing.urls')),

    path('tenant/prospectivemember/',include('prospectivemember.urls'))

]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)