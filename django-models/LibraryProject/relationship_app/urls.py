from django.urls import path
from relationship_app import views
from relationship_app.views import LibraryDetail, SignUpView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns=[
    path('list_books/', views.list_books, name='list_books'),
    path('library_detail/', LibraryDetail.as_view, name='library_detail'),
    path('login/', LoginView.as_view(template_name='template/relationship_app/login.html'), name='login'),
    path('register/', SignUpView.as_view, name='register'),
    path('logout/', LogoutView.as_view(template_name='template/relationship_app/logout.html'), name='logout') 
]