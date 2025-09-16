from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Book

# View books
@permission_required('bookshelf.can_view', raise_exception=True)
def list_books(request):
    books = Book.objects.all()
    return render(request, 'books/list.html', {'books': books})

# Create book
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        Book.objects.create(title=title, author=author)
    return render(request, 'books/create.html')

# Edit book
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.save()
    return render(request, 'books/edit.html', {"book": book})

# Delete book
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return render(request, 'books/delete.html')


# SAFE
from django.db.models import Q

def search_books(request):
    query = request.GET.get("q", "")
    books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    return render(request, "books/search_results.html", {"books": books})
