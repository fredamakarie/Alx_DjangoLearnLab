from django.urls import path
from relationship_app import views
from .views import LibraryDetail, SignUpView, admin_view, librarian_view, member_view
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns=[
    path('list_books/', views.list_books, name='list_books'),
    path('library_detail/', LibraryDetail.as_view (template_name='relationship_app/library_detail.html')),
    path('login/', LoginView.as_view (template_name="relationship_app/login.html"), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path("member-dashboard/", member_view.member_view, name="member_view"),
    path("librarian-dashboard/", librarian_view.librarian_view, name="librarian_view"),
    path("admin-dashboard/", admin_view.admin_view, name="admin_view"),
     
]