from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'api/games/initialize/$', views.initialize_game, name='initialize_game'),
]