from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from foodieshare.models import *
from foodieshare.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse



def main_feed(request):
    posts = Post.objects.all().order_by('-created_at')
    likes = Like.objects.all()
    context_dict = {"posts": posts, "likes": likes}
    return render(request, 'foodieshare/main_feed.html', context=context_dict)


@login_required
def my_profile(request):
    user_profile, _ = UserProfile.objects.get_or_create(auth_user=request.user)
    post_form = PostForm()
    profile_form = UserProfileForm(instance=user_profile)

    if request.method == 'POST':
        form_type = request.POST.get('form_type', '')

        if form_type == 'post_form':
            post_form = PostForm(request.POST, request.FILES)
            if post_form.is_valid():
                new_post = post_form.save(commit=False)
                new_post.user = user_profile
                new_post.save()
                messages.success(request, "Your post has been created!")
                return redirect('foodieshare:main_feed')

        elif form_type == 'profile_form':
            profile_form = UserProfileForm(
                request.POST, request.FILES, instance=user_profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Your profile has been updated!")
                return redirect('foodieshare:my_profile')

    context = {
        'user_profile': user_profile,
        'post_form': post_form,
        'profile_form': profile_form,
    }
    return render(request, 'foodieshare/my_profile.html', context)

@login_required
def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    return render(request, 'foodieshare/user_profile.html', {'profile_user': profile_user})


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


def toggle_like(request, post_id):
    # Your logic to toggle the like...
    post = get_object_or_404(Post, pk=post_id)
    liked = False  # A flag to track if the post is liked or unliked in this request

    if request.method == 'POST':
        user_profile = request.user.userprofile
        like, created = Like.objects.get_or_create(post=post, user=user_profile)

        if not created:
            like.delete()  # Unlike the post
        else:
            liked = True

        total_likes = post.likes.count()

        return JsonResponse({'liked': liked, 'total_likes': total_likes})

    return JsonResponse({'error': 'Request must be POST.'}, status=400)

def about(request):
    total_recipes_shared = Post.objects.count()  # Get the total number of recipes
    # Assuming a community goal of 1000 recipes
    goal = 1000
    progress_percentage = (total_recipes_shared / goal) * 100

    context = {
        'total_recipes_shared': total_recipes_shared,
        'goal': goal,
        'progress_percentage': progress_percentage,
    }
    return render(request, 'foodieshare/about.html', context)

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user.userprofile  # Adjust based on your user profile relation
            comment.save()
            return redirect('foodieshare:post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()

    # Check if current user has liked the post
    user_like = None
    if request.user.is_authenticated:
        user_like = Like.objects.filter(post=post, user=request.user.userprofile).first()

    return render(request, 'foodieshare/post_detail.html', {
        'post': post,
        'comment_form': comment_form,
        'user_like': user_like
    })

def contact(request):
    return render(request, 'foodieshare/contact.html')