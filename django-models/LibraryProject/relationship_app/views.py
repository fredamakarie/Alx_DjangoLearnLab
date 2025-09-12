from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Book

def list_books(request):
      """Retrieves all books and renders a template displaying the list."""
      books = Book.objects.all()  # Fetch all book instances from the database
      context = {'list_books': books}  # Create a context dictionary with book list
      return render(request, 'books/list_books.html', context)

from django.views.generic import DetailView
from .models import Book

class LibraryDetail(DetailView):
  """A class-based view for displaying details of a specific book."""
  model = Book
  template_name = 'templates/relationship_app/library_detail.html'

  def get_context_data(self, **kwargs):
    """Injects additional context data specific to the book."""
    context = super().get_context_data(**kwargs)  # Get default context data
    book = self.get_object()  # Retrieve the current book instance
    context['average_rating'] = book.get_average_rating() 

