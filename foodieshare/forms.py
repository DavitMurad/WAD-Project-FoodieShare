from django import forms
from foodieshare.models import*
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        

class Post_Form(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_image', 'nutrition', 'recipe']
        widgets = {
            'nutrition': forms.Textarea(attrs={'rows': 3}),
            'recipe': forms.Textarea(attrs={'rows': 3}),
        }