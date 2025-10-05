from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from taggit.managers import TaggableManager


# Create your models here.
class Post (models.Model):
    title = models.CharField(max_length=200)
    content= models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author= models.ForeignKey(User, on_delete=models.CASCADE)
    tags =TaggableManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    class Meta:
        permissions = [
            ("can_add_post", "Can add posts"),
            ("can_change_post", "Can change posts"), 
            ("can_delete_post", "Can delete posts")]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author= models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
    
    class Meta:
        permissions = [
            ("can_add_comment", "Can add comments"),
            ("can_change_comment", "Can change comments"), 
            ("can_delete_comment", "Can delete comments")]
        
class Tag(models.Model):
    name = models.CharField(max_length=200)
    posts= models.ManyToManyField(Post)
    def __str__(self):
        return self.name

    
class UserProfile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user
    
  


# 🔔 Signal to auto-create a UserProfile when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:  # Only when a new User is created
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

