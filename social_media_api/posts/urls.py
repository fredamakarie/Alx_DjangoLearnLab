from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    PostListCreateView, PostDetailView, PostViewSet, FollowedPostsView,
    CommentListCreateView, CommentDetailView, like_post, unlike_post
)

router = DefaultRouter()
router.register(r'post_all', PostViewSet, basename='post_all') 

urlpatterns = [
    # Posts
    path('', PostListCreateView.as_view(), name='post-list-create'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),

    # Comments
    path('<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),

     # Likes
    path('<int:pk>/like/', like_post, name='like-post'),
    path('<int:pk>/unlike/', unlike_post, name='unlike-post'),
    path('feed/', FollowedPostsView.as_view(), name='followed-posts'),

]
