from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Book, Author


class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create an author and user for testing
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.author = Author.objects.create(name="George Orwell")

        # Authenticated client
        self.client = APIClient()
        self.client.login(username='testuser', password='testpass123')

        # URLs
        self.list_url = reverse('book-list')
        self.create_url = reverse('book-create')

        # Create a sample book
        self.book = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author
        )

        self.detail_url = reverse('book-detail', kwargs={'pk': self.book.pk})
        self.update_url = reverse('book-update', kwargs={'pk': self.book.pk})
        self.delete_url = reverse('book-delete', kwargs={'pk': self.book.pk})


    # ✅ Test: Create a new Book
    def test_create_book(self):
        data = {
            "title": "Animal Farm",
            "publication_year": 1945,
            "author": self.author.id
        }
        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(response.data["title"], "Animal Farm")


    # ✅ Tes
