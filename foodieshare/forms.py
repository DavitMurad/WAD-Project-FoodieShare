from django import forms
from foodieshare.models import*
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_image', 'description', 'recipe']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'recipe': forms.Textarea(attrs={'rows': 3}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']