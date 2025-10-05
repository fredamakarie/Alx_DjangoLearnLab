from rest_framework import generics, permissions, filters, status, serializers
from rest_framework.response import Response
from datetime import datetime
from .models import Book
from .serializers import BookSerializer


# 🔹 1. ListView with filtering and search support
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Allow filtering and searching
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author__name']  # search by title or author name
    ordering_fields = ['publication_year', 'title']  # allow ordering by year/title

    def get_queryset(self):
        """
        Optionally filter books by publication_year query param
        Example: /books/?year=2020
        """
        queryset = super().get_queryset()
        year = self.request.query_params.get('year')
        if year:
            queryset = queryset.filter(publication_year=year)
        return queryset


# 🔹 2. CreateView — Custom validation & permissions
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can create

    def perform_create(self, serializer):
        """
        Extra validation or logic before saving.
        For example, prevent duplicate titles per author.
        """
        author = serializer.validated_data.get('author')
        title = serializer.validated_data.get('title')

        if Book.objects.filter(title=title, author=author).exists():
            raise serializers.ValidationError(
                {"detail": "This author already has a book with this title."}
            )

        # Custom logic (you could log creation or assign defaults here)
        serializer.save()


# 🔹 3. UpdateView — Handle partial updates and permissions
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # must be logged in

    def update(self, request, *args, **kwargs):
        """
        Custom response & validation on update
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Example: prevent setting future publication year
        year = serializer.validated_data.get('publication_year', instance.publication_year)
        if year > datetime.now().year:
            return Response(
                {"error": "Publication year cannot be in the future."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.perform_update(serializer)
        return Response({
            "message": "Book updated successfully!",
            "book": serializer.data
        })


# 🔹 4. DetailView — Retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# 🔹 5. DeleteView — Remove a book
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer