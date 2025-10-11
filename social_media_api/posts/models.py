from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, )
    title = models.CharField(max_length=250)
    content = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User,)
    content = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

class Like(models.Model):
    post = post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User,)