# blog/urls.py
from django.urls import path
from .views import (
    PostListView, PostDetailView,
    PostCreateView, PostUpdateView, PostDeleteView, CommentCreateView, CommentDeleteView, CommentUpdateView, SearchResultsView, TagListView, LoginView, LogoutView, SignUpView, ProfileUpdateView,
)

urlpatterns = [
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile-edit'),
    path('login/', LoginView.as_view (template_name='blog/login.html'), name='login'),
    path('register/', SignUpView.as_view (template_name='blog/register.html')),
    path('logout/', LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('posts/int:post_id/comment/new/', CommentCreateView.as_view(), name='comment-create'),
    path('posts/int:post_id/comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('posts/int:post_id/comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('search/', SearchResultsView.as_view(), name='search-results'),  
    path('tags/<str:tag_name>/', TagListView.as_view(), name='posts-by-tag'),
]
