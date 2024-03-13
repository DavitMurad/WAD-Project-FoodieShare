from django.shortcuts import render
from django.http import HttpResponse
from foodieshare.models import *

def main_feed(request):
    posts = Post.objects.all()
    likes = Like.objects.all()
    context_dict = {"posts" : posts, "likes" : likes}
    return render(request, 'foodieshare/main_feed.html',context=context_dict)

def my_profile(request):
    return render(request, 'foodieshare/my_profile.html')

def user_profile(request):
    return render(request, 'foodieshare/user_profile.html')


def register(request):
    return render(request, 'foodieshare/register.html')

def login(request):
    return render(request, 'foodieshare/login.html')