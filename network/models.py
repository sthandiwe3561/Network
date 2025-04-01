from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="Profile_user")
    username = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    bio = models.TextField()
    
    def __str__(self):
        return f"{self.username} by {self.user.username}"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    content = models.TextField()
    image = models.ImageField(upload_to="posts/", blank=True, null=True)  # Optional field
    created_at = models.DateTimeField(auto_now_add=True)
    hide = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)  # Users who liked the post

    def __str__(self):
        return f"Post by {self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")  # User who follows
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")  # User being followed
    follow_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  # Prevent duplicate follow relationships

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"