from .models import Librarian, Library, Book


# Query all books by a specific author.
author_books= Book.objects.filter(author='Jane Austen')

# List all books in a library.
books= Library.objects.all()

# Retrieve the librarian for a library
librarian_name= Librarian.objects.all()