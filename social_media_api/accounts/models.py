from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Followers(models.Model):
    followers = models.IntegerField(null=True)

# Custom User model
class CustomUser(AbstractUser):
    bio = models.TextField(max_length=1500)
    profile_photo = models.ImageField(upload_to="profile_photos/", null=True, blank=True)
    followers = models.ManyToManyField(Followers, symmetrical=False)
  

    def __str__(self):
        return self.username