from django.urls import path
from foodieshare import views

app_name = 'foodieshare'
urlpatterns = [
path('', views.main_feed, name='main_feed'),
]