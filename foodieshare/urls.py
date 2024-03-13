from django.urls import path
from foodieshare import views

app_name = 'foodieshare'
urlpatterns = [
    path('', views.main_feed, name='main_feed'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('user_profile/', views.user_profile, name="user_profile"),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
]
