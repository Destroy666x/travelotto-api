from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'api/games/initialize/$', views.initialize_game, name='initialize_game'),
    path('api/games/<int:game_id>/visit/<int:location_id>/', views.visit_location, name='visit_location'),
    path('api/games/<int:game_id>/answer/<int:location_id>/', views.answer_question, name='answer_question'),
]