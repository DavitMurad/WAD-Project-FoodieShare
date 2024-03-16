from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from foodieshare.models import*
from foodieshare.forms import Post_Form, UserRegisterForm
from django.contrib import messages



def main_feed(request):
    posts = Post.objects.all()
    likes = Like.objects.all()
    context_dict = {"posts": posts, "likes": likes}
    return render(request, 'foodieshare/main_feed.html', context=context_dict)

def my_profile(request):
    user_profile = UserProfile.objects.get(auth_user=request.user)

    if request.method == 'POST':
        post_form = Post_Form(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = user_profile 
            post.save()
            return redirect('foodieshare:main_feed')
    else:
        post_form = Post_Form() 

    context = {'user_profile': user_profile, 'post_form': post_form}
    return render(request, 'foodieshare/my_profile.html', context)

def user_profile(request):
    return render(request, 'foodieshare/user_profile.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('foodieshare:login')
    else:
        form = UserRegisterForm()
    return render(request, 'foodieshare/register.html', {'form': form})

def login(request):
    return render(request, 'foodieshare/login.html')


def add_comment_to_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == "POST":
        content = request.POST.get('content')
        comment = Comment.objects.create(
            post=post, author=request.user, content=content)
        comment.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
