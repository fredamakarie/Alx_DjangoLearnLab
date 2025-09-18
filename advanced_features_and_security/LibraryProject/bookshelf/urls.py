from django.urls import path
from bookshelf import views


urlpatterns=[
    path('book_list/', views.book_list, name='book_list'),
    
]