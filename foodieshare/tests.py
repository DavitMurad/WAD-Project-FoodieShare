from django.test import TestCase, Client
from django.db.utils import IntegrityError
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date
from django.contrib.auth.models import User
from foodieshare.models import UserProfile
from foodieshare.models import Post
from foodieshare.models import Comment
from foodieshare.models import Like
from foodieshare.forms import UserRegisterForm
from foodieshare.forms import PostForm
from foodieshare.forms import UserProfileForm
import json

class UserProfileModelTestCase(TestCase):
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


class PostModelTestCase(TestCase):
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


class CommentModelTestCase(TestCase):
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


class LikeModelTestCase(TestCase):
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
        self.client = Client()
        self.user = User.objects.create(username='testuser')
        self.user_profile = UserProfile.objects.create(auth_user=self.user)
        self.post = Post.objects.create(user= self.user_profile, nutrition='test nutrition', recipe='test recipe')

    def test_main_feed_view(self):
        url = reverse('main_feed')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'foodieshare/main_feed.html')

        self.assertIn('posts', response.context)
        self.assertIn('likes', response.context)


class MyProfileViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_my_profile_view(self):
        url = reverse('foodieshare:my_profile')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'foodieshare/my_profile.html')

        self.assertIn('post_form', response.context)
        self.assertIn('profile_form', response.context)

    def test_post_creation(self):
        url = reverse('foodieshare:my_profile')
        post_data = {
            'form_type': 'post_form',
            'nutrition': 'test nutrition',
            'recipe': 'test recipe'
        }
        response = self.client.post(url, post_data, format='multipart')

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(user=self.user.userprofile).exists())

    def test_profile_picture_update(self):
        url = reverse('foodieshare:my_profile')

        test_profile_image = SimpleUploadedFile (
            name='meal.jpg',
            content=open('static/foodieshare/images/meal.jpg', 'rb').read(),
            content_type='image/jpeg'
        )

        profile_data = {
            'form_type': 'profile_form',
            'profile_picture': test_profile_image,
        }

        response = self.client.post(url, profile_data, format='multipart')
        self.assertEqual(response.status_code, 302)

        updated_profile = UserProfile.objects.get(auth_user=self.user)
        self.assertEqual(updated_profile.profile_picture.name[0:17], 'profile_pics/meal')


class UserProfileViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_user_profile_view(self):
        url = reverse('foodieshare:user_profile', args=['testuser'])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'foodieshare/user_profile.html')

        self.assertIn('profile_user', response.context)
        self.assertEqual(response.context['profile_user'], self.user)

    def test_user_profile_not_found(self):
        url = reverse('foodieshare:user_profile', args=['nonexistentuser'])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_profile(self):
        url = reverse('foodieshare:register')
        data = {
            'username': 'testuser',
            'email': 'test@testuser.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('foodieshare:login'))

    def test_register_invalid_data(self):
        url = reverse('foodieshare:register')
        data = {}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', 'This field is required.')

    def test_register_get_form(self):
        url = reverse('foodieshare:register')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'foodieshare/register.html')

    
class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_view(self):
        url = reverse('foodieshare:login')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'foodieshare/login.html')


class AddCommentToPostViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(auth_user=self.user)
        self.post = Post.objects.create(user= self.user_profile, nutrition='test nutrition', recipe='test recipe')

    def test_add_comment_to_post(self):
        url = reverse('foodieshare:add_comment_to_post', args=[self.post.id])
        data = {'content': 'test content'}

        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(post=self.post, user=self.user_profile, content='test content').exists())
        

class ToggleLikeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(auth_user=self.user)
        self.post = Post.objects.create(user= self.user_profile, nutrition='test nutrition', recipe='test recipe')

    def test_successful_like_creation(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('foodieshare:toggle_like'), {'post_id':self.post.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['action'], 'liked')

        self.assertTrue(Like.objects.filter(post=self.post, user=self.user_profile).exists())

    def test_successful_like_deletion(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('foodieshare:toggle_like'), {'post_id':self.post.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = self.client.post(reverse('foodieshare:toggle_like'), {'post_id':self.post.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['action'], 'unliked')

        self.assertFalse(Like.objects.filter(post=self.post, user=self.user_profile).exists())

    def test_invalid_requests(self):
        response = self.client.get(reverse('foodieshare:toggle_like'), {'post_id':self.post.id})
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['status'], 'failed')

        response = self.client.post(reverse('foodieshare:toggle_like'), {'post_id': self.post.id})
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['status'], 'failed')


class UserRegisterTestFormTestCase(TestCase):
    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@testuser.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        form = UserRegisterForm(data=form_data)

        self.assertTrue(form.is_valid())

        new_user = form.save(commit=False)
        self.assertIsInstance(new_user, User)
        self.assertEqual(new_user.username, 'testuser')
        self.assertEqual(new_user.email, 'test@testuser.com')

    def test_invalid_form(self):
        form_data = {
            'username': '',
            'email': 'invalidemailformat',
            'password1': 'testpassword',
            'password2': '',
        }
        form = UserRegisterForm(data=form_data)

        self.assertFalse(form.is_valid())

        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password2', form.errors)


class PostFormTestCase(TestCase):
    def test_valid_form(self):
        form_data = {
            'post_image': 'testimage.jpg',
            'nutrition': 'test nutrition',
            'recipe': 'test recipe',
        }
        form = PostForm(data=form_data)

        self.assertTrue(form.is_valid())

        new_post = form.save(commit=False)
        self.assertIsInstance(new_post, Post)
        self.assertEqual(new_post.nutrition, 'test nutrition')
        self.assertEqual(new_post.recipe, 'test recipe')

    def test_invalid_form(self):
        form_data = {}
        form = PostForm(data=form_data)

        self.assertFalse(form.is_valid())

        self.assertIn('nutrition', form.errors)
        self.assertIn('recipe', form.errors)

    def test_form_widgets(self):
        form = PostForm()

        self.assertEqual(form.fields['nutrition'].widget.__class__.__name__, 'Textarea')
        self.assertEqual(form.fields['nutrition'].widget.attrs.get('rows'), 3)

        self.assertEqual(form.fields['recipe'].widget.__class__.__name__, 'Textarea')
        self.assertEqual(form.fields['recipe'].widget.attrs.get('rows'), 3)


class UserProfileFormTestCase(TestCase):
    def test_valid_form(self):
        test_image = open('static/foodieshare/images/meal.jpg', 'rb')
        form_data = {
            'profile_picture': SimpleUploadedFile('meal.jpg', test_image.read()),
        }
        form = UserProfileForm(data=form_data, files=form_data)

        self.assertTrue(form.is_valid())

        new_profile = form.save(commit=False)
        self.assertIsInstance(new_profile, UserProfile)
        self.assertEqual(new_profile.profile_picture.name[0:17], 'meal.jpg')


