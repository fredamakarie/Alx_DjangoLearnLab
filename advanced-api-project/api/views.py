from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Book
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import BookSerializer



class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # ✅ enable filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # ✅ specify fields you want to filter by (exact matches)
    filterset_fields = ['author', 'publication_year']

    # ✅ specify fields you want to search in (partial matches)
    search_fields = ['title', 'author__name']

    # ✅ specify fields you want to order by
    ordering_fields = ['publication_year', 'title']
    ordering = ['title']  # default ordering

# 🔹 DetailView — show one book by ID
class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'


# 🔹 CreateView — create a new book
class BookCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'publication_year', 'author']
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('book-list')
    permission_required = 'app.add_book'  # check add_book permission

    def form_valid(self, form):
        # extra validation or logic before saving
        if form.cleaned_data['publication_year'] > 2025:
            form.add_error('publication_year', 'Publication year cannot be in the future.')
            return self.form_invalid(form)
        return super().form_valid(form)


# 🔹 UpdateView — edit existing book
class BookUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'publication_year', 'author']
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('book-list')
    permission_required = 'app.change_book'

    def form_valid(self, form):
        if form.cleaned_data['publication_year'] > 2025:
            form.add_error('publication_year', 'Publication year cannot be in the future.')
            return self.form_invalid(form)
        return super().form_valid(form)


# 🔹 DeleteView — delete a book
class BookDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'
    success_url = reverse_lazy('book-list')
    permission_required = 'app.delete_book'
