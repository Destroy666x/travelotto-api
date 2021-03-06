"""lotto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls import url
from . import views
from rest_framework import routers
from api.api import *

router = routers.DefaultRouter()
router.register(r'games', GameViewSet)
router.register(r'users', UserViewSet)
router.register(r'user-profiles', UserProfileViewSet)
router.register(r'game-locations', GameLocationViewSet)
router.register(r'game-invitations', GameInvitationViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'lotteries', LotteryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    url('^api/', include(router.urls)),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^rest-auth/twitter/$', views.TwitterLogin.as_view(), name='twitter_login'),
    url(r'^rest-auth/facebook/$', views.FacebookLogin.as_view(), name='fb_login'),
]
