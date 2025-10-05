# blog/urls.py
from django.urls import path
from .views import (
    PostListView, PostDetailView,
    PostCreateView, PostUpdateView, PostDeleteView, CommentCreateView, CommentDeleteView, CommentUpdateView, SearchResultsView, TagListView,
)

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('comment/new/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('search/', SearchResultsView.as_view(), name='search-results'),  
    path('tags/<str:tag_name>/', TagListView.as_view(), name='posts-by-tag'),
]
