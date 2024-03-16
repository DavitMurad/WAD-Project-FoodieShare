from django.db import models
from django.contrib.auth.models import User as AuthUser


class UserProfile(models.Model):
    auth_user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    bio = models.CharField(max_length=20)
    profile_picture= models.ImageField(default = "https://t4.ftcdn.net/jpg/02/29/75/83/360_F_229758328_7x8jwCwjtBMmC6rgFzLFhZoEpLobB6L8.jpg")

    def __str__(self):
        return self.auth_user.username


class Post(models.Model):
    user = models.ForeignKey(
        UserProfile, related_name='posts', on_delete=models.CASCADE)
    post_image= models.ImageField(default = "https://t4.ftcdn.net/jpg/02/29/75/83/360_F_229758328_7x8jwCwjtBMmC6rgFzLFhZoEpLobB6L8.jpg")
    nutrition = models.TextField()
    recipe = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Post {self.id} by {self.user.auth_user.username}"


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(
        UserProfile, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Comment {self.id} by {self.user.auth_user.username} on Post {self.post.id}"


class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes',
                             on_delete=models.CASCADE)
    user = models.ForeignKey(
        UserProfile, related_name='likes', on_delete=models.CASCADE)

    def __str__(self):
        return f"Like by {self.user.auth_user.username} on Post {self.post.id}"

    class Meta:
        unique_together = ('post', 'user') 
