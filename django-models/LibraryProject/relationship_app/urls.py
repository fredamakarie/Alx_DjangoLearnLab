from django.urls import path
from . import views

urlpatterns=[
    path('list_books/', views.list_books, name='list_books'),
    path('library_detail/', views.LibraryDetail, name='library_detail'),
    path('login/', views.library_detail, name='login'),
    path('lregister/', views.library_detail, name='register'),
    path('logout', views.library_detail, name='logout')
]