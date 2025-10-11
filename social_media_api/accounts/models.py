from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# Custom User model
class CustomUser(AbstractUser):
    bio = models.TextField(max_length=1500)
    profile_photo = models.ImageField(upload_to="profile_photos/", null=True, blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following',
        blank=True)
    following =  models.ManyToManyField('self', symmetrical=False, related_name='following',
        blank=True)

    def __str__(self):
        return self.username