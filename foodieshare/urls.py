from django.urls import path
from foodieshare import views

app_name = 'foodieshare'
urlpatterns = [
    path('', views.main_feed, name='main_feed'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
]
