from django.shortcuts import render
from .models import Book,Library
from django.views.generic import DetailView

# Create your views here.


def list_books(request):
      """Retrieves all books and renders a template displaying the list."""
      books = Book.objects.all()  # Fetch all book instances from the database
      context = {'list_books': books}  # Create a context dictionary with book list
      return render(request, 'templates/relationship_app/list_books.html', context)



class LibraryDetail(DetailView):
  """A class-based view for displaying details of a specific Library."""
  model = Library
  template_name = 'templates/relationship_app/library_detail.html'

  def get_context_data(self, **kwargs):
    """Injects additional context data specific to the book."""
    context = super().get_context_data(**kwargs)  # Get default context data
    book = self.get_object()  # Retrieve the current book instance
    context['books'] = book.get_books() 

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'template/relationship_app/register.html'

