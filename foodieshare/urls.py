from django.urls import path
from foodieshare import views
from django.contrib.auth import views as auth_views
from .views import toggle_like


app_name = 'foodieshare'
urlpatterns = [
    path('', views.main_feed, name='main_feed'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('user_profile/', views.user_profile, name="user_profile"),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', auth_views.LoginView.as_view(template_name='foodieshare/login.html'), name='login'),   
    path('logout/', auth_views.LogoutView.as_view(template_name='foodieshare/logout.html'), name='logout'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),

    path('post/<int:post_id>/toggle_like/', toggle_like, name='toggle_like'),
        
    path('post/<int:post_id>/add_comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
]
