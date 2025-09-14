from django.urls import path
from relationship_app import views
from relationship_app.views import LibraryDetail, SignUpView
from django.contrib.auth.views import LoginView, LogoutView
from . import admin_view, librarian_view, member_view

urlpatterns=[
    path('list_books/', views.list_books, name='list_books'),
    path('library_detail/', LibraryDetail.as_view (template_name='relationship_app/library_detail.html')),
    path('login/', LoginView.as_view (template_name='relationship_app/login.html'), name='login'),
    path('register/', SignUpView.as_view (template_name='relationship_app/register.html')),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path("member-dashboard/", member_view.member_view, name="member_view"),
    path("librarian-dashboard/", librarian_view.librarian_view, name="librarian_view"),
    path("admin-dashboard/", admin_view.admin_view, name="admin_view") 
]