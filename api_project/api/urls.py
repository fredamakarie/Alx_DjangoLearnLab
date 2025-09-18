# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BookList
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')  # Register the BookViewSet with the router

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('api/', include(router.urls)),  
    path('api/token/', obtain_auth_token, name='api_token_auth')
]   

