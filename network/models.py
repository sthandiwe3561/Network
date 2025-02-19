from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class ProfileSetup(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile_pics/", default="default.jpg")
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100,blank=True)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"