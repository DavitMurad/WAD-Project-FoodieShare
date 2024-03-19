from django.urls import path
from foodieshare import views
from django.contrib.auth import views as auth_views


app_name = 'foodieshare'
urlpatterns = [
    path('', views.main_feed, name='main_feed'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('user_profile/', views.user_profile, name="user_profile"),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='foodieshare/login.html'), name='login'),
    path('post/<int:post_id>/add_comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('logout/', auth_views.LogoutView.as_view(template_name='foodieshare/logout.html'), name='logout'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('toggle_like/', views.toggle_like, name='toggle_like'),

]
