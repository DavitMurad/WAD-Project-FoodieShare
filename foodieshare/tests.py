from django.test import TestCase, RequestFactory
from django.db.utils import IntegrityError
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from foodieshare.models import UserProfile
from foodieshare.models import Post
from foodieshare.models import Comment
from foodieshare.models import Like
from foodieshare.views import main_feed

class UserProfileTestCase(TestCase):
    def test_profile_creation(self):
        user = User.objects.create(username='testuser')
        profile = UserProfile.objects.create(auth_user=user, bio='test bio')

        self.assertEqual(profile.auth_user.username, 'testuser')
        self.assertEqual(profile.bio, 'test bio')

    def test_profile_retrieval(self):
        user = User.objects.create(username='testuser')
        profile = UserProfile.objects.create(auth_user=user, bio='test bio')

        retrieval_profile = UserProfile.objects.get(auth_user=user)

        self.assertEqual(profile, retrieval_profile)

    def test_profile_update(self):
        user = User.objects.create(username='testuser')
        profile = UserProfile.objects.create(auth_user=user, bio='test bio')

        profile.bio = 'updated bio'
        profile.save()

        updated_profile = UserProfile.objects.get(auth_user=user)
        self.assertEqual(updated_profile.bio, 'updated bio')

    def test_profile_deletion(self):
        user = User.objects.create(username='testuser')
        profile = UserProfile.objects.create(auth_user=user, bio='test bio')

        user.delete()

        with self.assertRaises(UserProfile.DoesNotExist):
            UserProfile.objects.get(auth_user=user)

    def test_default_values(self):
        user = User.objects.create(username='testuser')
        profile = UserProfile.objects.create(auth_user=user)

        self.assertEqual(profile.date_of_birth, date.today())
        self.assertEqual(profile.profile_picture.name, 'user.jpg')


class PostTestCase(TestCase):
    def test_post_creation(self):
        user = User.objects.create(username='testuser')
        user_profile = UserProfile.objects.create(auth_user=user)
        post = Post.objects.create(user=user_profile, nutrition='test nutrition', recipe='test recipe')

        self.assertEqual(post.user.auth_user.username, 'testuser')
        self.assertEqual(post.nutrition, 'test nutrition')
        self.assertEqual(post.recipe, 'test recipe')

    def test_post_retrieval(self):
        user = User.objects.create(username='testuser')
        user_profile = UserProfile.objects.create(auth_user=user)
        post = Post.objects.create(user=user_profile, nutrition='test nutrition', recipe='test recipe')

        retrieved_post = Post.objects.get(user=user_profile)

        self.assertEqual(post, retrieved_post)

    def test_post_deletion(self):
        user = User.objects.create(username='testuser')
        user_profile = UserProfile.objects.create(auth_user=user)
        post = Post.objects.create(user=user_profile, nutrition='test nutrition', recipe='test recipe')

        user_profile.delete()

        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(user=user_profile)

    def test_default_values(self):
        user = User.objects.create(username='testuser')
        user_profile = UserProfile.objects.create(auth_user=user)
        post = Post.objects.create(user=user_profile)

        self.assertEqual(post.post_image.name, 'meal.jpg')


class CommentTestCase(TestCase):
    def test_comment_creation(self):
        user = User.objects.create(username='testuser')
        user_profile = UserProfile.objects.create(auth_user=user)
        post = Post.objects.create(user=user_profile, nutrition='test nutrition', recipe='test recipe')
        comment = Comment.objects.create(post=post, user=user_profile, content='test comment')

        self.assertEqual(comment.post, post)
        self.assertEqual(comment.user, user_profile)
        self.assertEqual(comment.content, 'test comment')
    
    def test_comment_retrieval(self):
        user = User.objects.create(username='testuser')
        user_profile = UserProfile.objects.create(auth_user=user)
        post = Post.objects.create(user=user_profile, nutrition='test nutrition', recipe='test recipe')
        comment = Comment.objects.create(post=post, user=user_profile, content='test comment')

        retrieved_comment = Comment.objects.get(post=post, user=user_profile)

        self.assertEqual(comment, retrieved_comment)

    def test_comment_deletion(self):
        user = User.objects.create(username='testuser')
        user_profile = UserProfile.objects.create(auth_user=user)
        post = Post.objects.create(user=user_profile, nutrition='test nutrition', recipe='test recipe')
        comment = Comment.objects.create(post=post, user=user_profile, content='test comment')

        post.delete()

        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(pk=comment.pk)


class LikeTestCase(TestCase):
    def test_like_creation(self):
        user = User.objects.create(username='testuser')
        user_profile = UserProfile.objects.create(auth_user=user)
        post = Post.objects.create(user=user_profile, nutrition='test nutrition', recipe='test recipe')
        like = Like.objects.create(post=post, user=user_profile)

        self.assertEqual(like.post, post)
        self.assertEqual(like.user, user_profile)

    def test_like_retrieval(self):
        user = User.objects.create(username='testuser')
        user_profile = UserProfile.objects.create(auth_user=user)
        post = Post.objects.create(user=user_profile, nutrition='test nutrition', recipe='test recipe')
        like = Like.objects.create(post=post, user=user_profile)

        retrieved_like = Like.objects.get(post=post, user=user_profile)

        self.assertEqual(like, retrieved_like)

    def test_like_deletion(self):
        user = User.objects.create(username='testuser')
        user_profile = UserProfile.objects.create(auth_user=user)
        post = Post.objects.create(user=user_profile, nutrition='test nutrition', recipe='test recipe')
        like = Like.objects.create(post=post, user=user_profile)

        post.delete()

        with self.assertRaises(Like.DoesNotExist):
            Like.objects.get(pk=like.pk)

    def test_unique_constraint(self):
        user = User.objects.create(username='testuser')
        user_profile = UserProfile.objects.create(auth_user=user)
        post = Post.objects.create(user=user_profile, nutrition='test nutrition', recipe='test recipe')
        like = Like.objects.create(post=post, user=user_profile)

        with self.assertRaises(IntegrityError):
            Like.objects.create(post=post, user=user_profile)


class MainFeedViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username='testuser')
        self.post = Post.objects.create(user= self.user, nutrition='test nutrition', recipe='test recipe')

    def test_main_feed_view(self):
        url = reverse('main_feed')
        request = self.factory.get(url)
        response = main_feed(request)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'foodieshare/main_feed.html')
