import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wad_project.settings')

import django
django.setup()

from foodieshare.models import *
from django.utils import timezone
from django.contrib.auth.models import User


def create_user(username, email, password, date_of_birth, bio, profile_picture):
    user = User.objects.create_user(
        username=username, email=email, password=password)
    user_profile = UserProfile.objects.create(
        auth_user=user,
        date_of_birth=date_of_birth,
        bio=bio,
        profile_picture=profile_picture
    )
    return user_profile


def create_post(user_profile, post_image, description, recipe):
    post = Post.objects.create(
        user=user_profile,
        post_image=post_image,
        description=description,
        recipe=recipe,
        created_at=timezone.now()
    )
    return post


def create_comment(user_profile, post, content):
    comment = Comment.objects.create(
        user=user_profile,
        post=post,
        content=content
    )
    return comment


def create_like(user_profile, post):
    like = Like.objects.create(
        user=user_profile,
        post=post
    )
    return like


def populate_database(num_users=5, posts_per_user=3, comments_per_post=2, likes_per_post=1):
    for i in range(num_users):

        username = f'user{i}'
        email = f'user{i}@example.com'
        user_profile = create_user(
            username=username,
            email=email,
            password='testpassword123',
            date_of_birth='1990-01-01',
            bio=f'User {i} bio...',
            profile_picture='path/to/default/profile_pic.jpg'
        )

        for j in range(posts_per_user):
            post = create_post(
                user_profile=user_profile,
                post_image='path/to/default/post_image.jpg',
                description='description...',
                recipe=f'Recipe details for post {j}...'
            )

            for k in range(comments_per_post):
                create_comment(
                    user_profile=user_profile,
                    post=post,
                    content=f'Comment {k} on Post {j}...'
                )

            for l in range(likes_per_post):
                create_like(
                    user_profile=user_profile,
                    post=post
                )

    print(f"Created {num_users} users, {num_users * posts_per_user} posts, {num_users * posts_per_user * comments_per_post} comments, and {num_users * posts_per_user * likes_per_post} likes.")


if __name__ == '__main__':
    populate_database(num_users=10, posts_per_user=5,
                      comments_per_post=2, likes_per_post=1)
