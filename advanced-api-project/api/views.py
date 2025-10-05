from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Book


# 🔹 ListView — shows all books
class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'   # customize template
    context_object_name = 'books'            # context name in template
    ordering = ['title']                     # optional ordering


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
