from django.shortcuts import render
from django.views.generic.detail import DetailView
from models import Book

# Create your views here.

def list_books(request):
      """Retrieves all books and renders a template displaying the list."""
      books = Book.objects.all()  # Fetch all book instances from the database
      context = {'list_books': books}  # Create a context dictionary with book list
      return render(request, 'relationship_app/list_books.html', context)


class BookDetail(DetailView):
    """A class-based view for displaying details of a specific Book."""
    model = Book
    template_name = 'relationship_app/Book_detail.html'  

    def get_context_data(self, **kwargs):
        """Inject additional context data specific to the Book."""
        context = super().get_context_data(**kwargs)
        Book = self.get_object()  # this is the Book instance

        # If Book has a ForeignKey to Book
        context ['books']= Book.books.all()

        return context
    

