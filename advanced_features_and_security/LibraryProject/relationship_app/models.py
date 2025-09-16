from django.db import models
from django.conf import settings
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
            ("can_delete_book", "Can delete books"),
            ("can_view", "Can view books")
            ]
    

    

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
    user= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role= models.CharField(max_length=20, choices=role_choices, default='Member')
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"





# 🔔 Signal to auto-create a UserProfile when a User is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # only create if not already existing (avoids duplicate issues)
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    # safeguard in case profile doesn’t exist yet
    if hasattr(instance, "userprofile"):
        instance.userprofile.save()


