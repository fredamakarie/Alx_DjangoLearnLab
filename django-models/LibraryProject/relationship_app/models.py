from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    class Meta:
        permissions = [
            ("can_add_book", "Can add books"),
            ("can_change_book", "Can change books"), 
            ("can_delete_book", "Can delete books")]
    

    

class Library(models.Model):
    name= models.CharField(max_length=200)
    books= models.ManyToManyField(Book)
    def __str__(self):
        return self.name
    

class Librarian(models.Model):
    name= models.CharField(max_length=200)
    library= models.OneToOneField(Library, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
    
class UserProfile(models.Model):
    role_choices=[
        ('Admin', 'Admin'),('Librarian', 'Librarian'),('Member', 'Member')
    ]
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    role= models.CharField(max_length=20, choices=role_choices, default='Member')
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"


# 🔔 Signal to auto-create a UserProfile when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:  # Only when a new User is created
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()




