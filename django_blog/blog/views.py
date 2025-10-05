
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, path
from django.views.generic import CreateView
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.views import LoginView, LogoutView


# Create your views here.

#POSTS
#post list
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

#post detail
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

#post creation
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    permission_required = 'blog.add_post'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
#post edit
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    permission_required = 'blog.change_post'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

#post deletion
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')
    permission_required = 'blog.delete_post'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


#COMMENTS
#comment creation
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    permission_required = 'blog.add_comment'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


#comment edit   
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    permission_required = 'blog.change_comment'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


#comment deletion
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_delete.html'
    success_url = reverse_lazy('post-list')
    permission_required = 'blog.delete_comment'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    

from django.db.models import Q

class SearchResultsView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()
        return Post.objects.none()

class TagListView(ListView):
    model = Post
    template_name = 'blog/tagged_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        tag_name = self.kwargs.get('tag_name')
        return Post.objects.filter(tags__name__iexact=tag_name)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_name'] = self.kwargs.get('tag_name')
        return context



@permission_required('blog.add_comment', raise_exception=True)
def create_comment(request):
    if request.method == "POST":
        content = request.POST.get("post")
        author = request.POST.get("author")
        Comment.objects.create(content=content, author=author)
    return render(request, 'comment/create.html')






#sign up, login and logout
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'blog/register.html'



urlpatterns = [
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]



def my_login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # start session
            return redirect("blog")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")



def my_logout_view(request):
    logout(request)
    return redirect("login")
