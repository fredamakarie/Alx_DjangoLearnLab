from .models import Librarian, Library, Book

# relationship_app/query_samples.py
import django
import os

# ✅ Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library

# ------------------------------------------------------------------
# 1️⃣ Query all books by a specific author
# ------------------------------------------------------------------
def get_books_by_author(author_name):
    try:
        author = Author.objects.get(name = author_name)
        Author.objects.filter(author=author)
        books = author.books.all()
        print(f"Books by {author.name}:")
        for book in books:
            print(f" - {book.title}")
    except Author.DoesNotExist:
        print(f"No author found with name '{author}'")

# ------------------------------------------------------------------
# 2️⃣ List all books in a library
# ------------------------------------------------------------------
def list_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in library '{library.name}':")
        for book in books:
            print(f" - {book.title}")
    except Library.DoesNotExist:
        print(f"No library found with name '{library_name}'")

# ------------------------------------------------------------------
# 3️⃣ Retrieve the librarian for a library
# ------------------------------------------------------------------
def get_librarian_for_library(librarian_name):
    try:
        library = Library.objects.get(name = librarian_name)
        Library.objects.filter(library=library)
        librarian = library.librarian
        print(f"Librarian for '{library.name}': {librarian.username}")
    except Library.DoesNotExist:
        print(f"No library found with name '{library}'")

# ------------------------------------------------------------------
# Run sample queries
# ------------------------------------------------------------------
if __name__ == "__main__":
    # Change these to match your data
    get_books_by_author("J.K. Rowling")
    list_books_in_library("Central Library")
    get_librarian_for_library("Central Library")
