from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics, permissions, filters, viewsets
from django.shortcuts import get_object_or_404
from .models import Post, Like
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerialize

# --- POST VIEWS ---

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']



    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(viewsets.Modelviewset):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        # Prevent changing the author
        if self.request.user != self.get_object().author:
            return Response({"error": "You can only edit your own posts."}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()


# --- COMMENT VIEWS ---

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id).order_by('-created_at')

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        serializer.save(author=self.request.user, post_id=post_id)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if self.request.user != self.get_object().author:
            return Response({"error": "You can only edit your own comments."}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    if Like.objects.filter(user=user, post=post).exists():
        return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

    Like.objects.create(user=request.user, post=post)

    # Create notification for post author
    if post.author != user:
        Notification.objects.create(
            recipient=post.author,
            actor=user,
            verb="liked your post",
            target=post,
        )

    return Response({"detail": "Post liked."}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    like = Like.objects.filter(user=user, post=post).first()

    if not like:
        return Response({"detail": "You haven’t liked this post yet."}, status=status.HTTP_400_BAD_REQUEST)

    like.delete()
    return Response({"detail": "Post unliked."}, status=status.HTTP_200_OK)
