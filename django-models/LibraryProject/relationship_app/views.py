from django.shortcuts import render, redirect
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView



# Create your views here.


def list_books(request):
      """Retrieves all books and renders a template displaying the list."""
      books = Book.objects.all()  # Fetch all book instances from the database
      context = {'list_books': books}  # Create a context dictionary with book list
      return render(request, 'relationship_app/list_books.html', context)




class LibraryDetail(DetailView):
    """A class-based view for displaying details of a specific Library."""
    model = Library
    template_name = 'relationship_app/library_detail.html'  

    def get_context_data(self, **kwargs):
        """Inject additional context data specific to the library."""
        context = super().get_context_data(**kwargs)
        library = self.get_object()  # this is the Library instance

        # If Book has a ForeignKey to Library
        context ['books']= library.books.all()  

        return context


from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'template/relationship_app/register.html'

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.contrib.auth import login

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
from django.contrib.auth import authenticate, login


def my_login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # start session
            return redirect("member")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")

from django.contrib.auth import logout

def my_logout_view(request):
    logout(request)
    return redirect("login")


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book, Author


@permission_required("yourapp.can_add_book", raise_exception=True)
def add_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author_id = request.POST.get("author")
        author = get_object_or_404(Author, pk=author_id)

        Book.objects.create(title=title, author=author)
        return redirect("list_books")

    authors = Author.objects.all()  # to build a dropdown in template
    return render(request, "add_book.html", {"authors": authors})


@permission_required("yourapp.can_change_book", raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        book.title = request.POST.get("title")
        author_id = request.POST.get("author")
        book.author = get_object_or_404(Author, pk=author_id)
        book.save()
        return redirect("list_books")

    authors = Author.objects.all()
    return render(request, "edit_book.html", {"book": book, "authors": authors})


@permission_required("yourapp.can_delete_book", raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("list_books")
    return render(request, "delete_book.html", {"book": book})
