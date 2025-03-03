from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class ProfileSetup(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(upload_to="profile_setup/", default="default.jpg")
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100,blank=True)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    content = models.TextField()
    image = models.ImageField(upload_to="posts/", blank=True, null=True, default="default.jpg")  # Optional field
    created_at = models.DateTimeField(auto_now_add=True)
    hide = models.BooleanField(default=False)

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