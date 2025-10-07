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



# relationship_app/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Book, Library, Author

# ---------------------------------------
# Helper functions for role checking
# ---------------------------------------
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'ADMIN'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'LIBRARIAN'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'MEMBER'


# ---------------------------------------
# Admin View
# ---------------------------------------
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin can manage all users, libraries, and books."""
    context = {
        'authors': Author.objects.all(),
        'books': Book.objects.all(),
        'libraries': Library.objects.all(),
    }
    return render(request, 'relationship_app/admin_dashboard.html', context)


# ---------------------------------------
# Librarian View
# ---------------------------------------
@login_required
@user_passes_test(is_librarian)
def librarian_dashboard(request):
    """Librarian can view and manage books in their library."""
    library = Library.objects.filter(librarian=request.user).first()
    context = {
        'library': library,
        'books': library.books.all() if library else [],
    }
    return render(request, 'relationship_app/librarian_dashboard.html', context)


# ---------------------------------------
# Member (User) View
# ---------------------------------------
@login_required
@user_passes_test(is_member)
def member_dashboard(request):
    """Member can view all available books and authors."""
    context = {
        'books': Book.objects.all(),
        'authors': Author.objects.all(),
    }
    return render(request, 'relationship_app/member_dashboard.html', context)
