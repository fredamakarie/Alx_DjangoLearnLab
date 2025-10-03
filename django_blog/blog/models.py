from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Post (models.Model):
    title = models.CharField(max_length=200)
    content= models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author= models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


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
        
class UserProfile(models.Model):
    user= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return f"{self.user}"

